from cgitb import enable
import tkinter as tk
import tkinter.ttk as ttk

from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import ( FigureCanvasTkAgg, NavigationToolbar2Tk)

from AstraBox.Views.HeaderPanel import HeaderPanel
import AstraBox.Models.ModelFactory as ModelFactory


class InfoPanel(tk.LabelFrame):
    def __init__(self, master, model) -> None:
        super().__init__(master, text= 'Race info')
        info = {
            'Exp:': model.data['ExpModel']['name'],
            'Equ:': model.data['EquModel']['name'],
            'Ray tracing:': model.data['RTModel']['name']
            }
        for key, value in info.items():
            var = tk.StringVar(master= self, value=value)
            label = tk.Label(master=self, text=key)
            label.pack(side = tk.LEFT, ipadx=10)		
            entry = tk.Entry(self, width=15, textvariable= var, state='disabled')
            entry.pack(side = tk.LEFT)

class RaceView(ttk.Frame):
 
    def __init__(self, master, model) -> None:
        super().__init__(master)        
        self.master = master
        title = f"Race: {model.name}"
        self.header_content = { "title": title, "buttons":[('Delete', self.delete_model), ('new windows', self.open_new_windows) ]}
        self.model = model
        self.model.load_model_data()
        self.hp = HeaderPanel(self, self.header_content)
        self.hp.grid(row=0, column=0, columnspan=5, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)
        self.columnconfigure(0, weight=1)        
        #self.rowconfigure(0, weight=1)    
        #self.label = ttk.Label(self,  text=f'name: {model.name}')
        #self.label.grid(row=1, column=0, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W)   

        ip = InfoPanel(self, model)
        ip.grid(row=2, column=0, columnspan=5, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=3, column=0, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)

        radial_data_view = RadialDataView(self.notebook, model= model)
        self.notebook.add(radial_data_view, text="Radial Data", underline=0, sticky=tk.NE + tk.SW)
        
        trajectory_view = TrajectoryView(self.notebook, model= model)
        self.notebook.add(trajectory_view, text="Trajectory", underline=0, sticky=tk.NE + tk.SW)

    def delete_model(self):
        ModelFactory.delete_model(self.model)
        
    def open_new_windows(self):
        new_window = tk.Toplevel(self.master)
        new_window.title("Race Window")
        new_window.geometry("1150x870")                
        model_view = RaceView(new_window, self.model)   
        model_view.grid(row=0, column=0, padx=20, sticky=tk.N + tk.S + tk.E + tk.W)     

    def destroy(self):
        print("RaceView destroy")
        super().destroy()   

class TrajectoryView(ttk.Frame):
    def __init__(self, master, model) -> None:
        super().__init__(master)  
        self.model = model
        self.trajectory_list = model.get_trajectory_list()
        self.rays_cache = {}
        if len(self.trajectory_list)>0: 
            plasma_bound = model.read_plasma_bound()
            self.index_var = tk.IntVar(master = self, value=0)
            self.index_var.trace_add('write', self.update_var)

            self.slider = tk.Scale(master=  self, variable = self.index_var, orient = tk.HORIZONTAL, from_=0, to=len(self.trajectory_list)-1, resolution=1)
            self.slider.grid(row=0, column=0, columnspan=2, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W) 
           
            rays, time_stamp  = model.get_rays(self.trajectory_list[0])
            self.index_1 = tk.IntVar(master = self, value=0)
            self.index_1.trace_add('write', self.update_var)
            self.slider_1 = tk.Scale(master=  self, variable = self.index_1, orient = tk.HORIZONTAL, from_=0, to=len(rays)-1, resolution=1 )
            self.slider_1.grid(row=1, column=0, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W) 

            self.index_2 = tk.IntVar(master = self, value=len(rays)-1)
            self.index_2.trace_add('write', self.update_var)
            self.slider_2 = tk.Scale(master=  self, variable = self.index_2, orient = tk.HORIZONTAL, from_=0, to=len(rays)-1, resolution=1 )
            self.slider_2.grid(row=1, column=1, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W) 

            self.plot = TrajectoryPlot(self, rays, time_stamp, plasma_bound)
            self.plot.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=4, padx=8)
            self.columnconfigure(0, weight=1)
            self.columnconfigure(1, weight=1)

    def update_var(self, var, indx, mode):
        index = self.index_var.get()
        i1 = self.index_1.get()
        i2 = i1 + self.index_2.get()
        
        if not index in self.rays_cache:
            print(f'{index} not in cache')
            self.rays_cache[index] = self.model.get_rays(self.trajectory_list[index])
        rays, time_stamp = self.rays_cache[index]
        if i2>len(rays):
            i2 = len(rays)
        self.plot.update(rays[i1:i2], time_stamp)
        pass


class TrajectoryPlot(ttk.Frame):
    def __init__(self, master, rays, time_stamp, plasma_bound) -> None:
        super().__init__(master)  
        self.R, self.Z = plasma_bound
        self.fig = plt.figure(figsize=(6,6))
        #self.fig.title(time_stamp)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title(time_stamp)
        self.ax.axis('equal')
        self.ax.plot(self.R, self.Z)
        for ray in rays:
            self.ax.plot(ray['R'], ray['Z'], alpha=0.5, linewidth=1)

        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=1, column=0)
        frame = ttk.Frame(self)
        frame.grid(row=0, column=0, sticky=tk.W)
        toobar = NavigationToolbar2Tk(self.canvas, frame)
        #tb = VerticalNavigationToolbar2Tk(canvas, frame)
        #canvas.get_tk_widget().grid(row=2, column=0)

    def update(self, rays, time_stamp):
        self.ax.clear()
        self.ax.set_title(time_stamp)
        self.ax.plot(self.R, self.Z)
        for ray in rays:
            self.ax.plot(ray['R'], ray['Z'], alpha=0.5, linewidth=1)
        self.canvas.draw()

    def destroy(self):
        print("SimplePlot destroy")
        if self.fig:
            plt.close(self.fig)
        super().destroy()   




class RadialDataView(ttk.Frame):
    def __init__(self, master, model) -> None:
        super().__init__(master)  
        self.model = model
        self.radial_data_list = model.get_radial_data_list()

        if len(self.radial_data_list)>0: 
            self.index_var = tk.IntVar(master = self, value=0)
            self.index_var.trace_add('write', self.update_var)

            self.slider = tk.Scale(master=  self, variable = self.index_var, orient = tk.HORIZONTAL, from_=0, to=len(self.radial_data_list)-1, resolution=1, length = 250 )
            self.slider.grid(row=0, column=0, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W)       
 
            profiles = self.get_profiles(0)
            self.plot = SimplePlot(self, profiles)
            self.plot.grid(row=1, column=0, sticky=tk.W, pady=4, padx=8)

    def get_profiles(self, index):
        file = self.radial_data_list[index]
        print(f'{file} {index}')
        return self.model.read_radial_data(file)

    def update_var(self, var, indx, mode):
        profiles = self.get_profiles(self.index_var.get())
        self.plot.update(profiles)


class SimplePlot(ttk.Frame):
    def __init__(self, master, profiles) -> None:
        super().__init__(master)  
        #self.fig, self.axs = plt.subplots(2, 2, figsize=(7, 6))
        self.fig = plt.figure(figsize=(7, 8))
        self.fig.suptitle(f'Astra radial data. Time={profiles["Time"]}')
        self.axs = self.fig.subplots(4, 1)
        
        # профили токов
        self.profile_J,    = self.axs[0].plot(profiles['a'], profiles['J'])
        self.profile_Johm, = self.axs[0].plot(profiles['a'], profiles['Johm'])
        self.profile_Jlh, = self.axs[0].plot(profiles['a'], profiles['Jlh'])
        self.axs[0].set_title("J, Johm, Jlh")

        # профили E
        self.profile_E, = self.axs[1].plot(profiles['E'])
        self.profile_En, = self.axs[1].plot(profiles['En'])
        self.axs[1].set_title("E, En")
    
        # профили мощности
        self.profile_Plh, = self.axs[2].plot(profiles['Plh'])
        self.profile_Poh, = self.axs[2].plot(profiles['Poh'])
        self.axs[2].set_title("Plh, Poh")
    
        # профили температуры
        self.profile_Te, = self.axs[3].plot(profiles['Te'])
        #self.profile_Poh, = self.axs[2].plot(profiles['Poh'])
        self.axs[3].set_title("Te")

        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=1, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        frame = ttk.Frame(self)
        frame.grid(row=0, column=0, sticky=tk.W)
        toobar = NavigationToolbar2Tk(self.canvas, frame)
        #tb = VerticalNavigationToolbar2Tk(canvas, frame)
        #canvas.get_tk_widget().grid(row=2, column=0)

    def update(self, profiles):
        self.fig.suptitle(f'Astra radial data. Time={profiles["Time"]}')

        self.profile_J.set_ydata(profiles['J']) 
        self.profile_Johm.set_ydata(profiles['Johm']) 
        self.profile_Jlh.set_ydata(profiles['Jlh']) 
        self.axs[0].relim()
        self.axs[0].autoscale_view(True,True,True)        

        self.profile_E.set_ydata(profiles['E']) 
        self.profile_En.set_ydata(profiles['En']) 
        self.axs[1].relim()
        self.axs[1].autoscale_view(True,True,True) 

        self.profile_Plh.set_ydata(profiles['Plh']) 
        self.profile_Poh.set_ydata(profiles['Poh']) 
        self.axs[2].relim()
        self.axs[2].autoscale_view(True,True,True) 
        
        self.profile_Te.set_ydata(profiles['Te']) 
        self.axs[3].relim()
        self.axs[3].autoscale_view(True,True,True)         

        self.canvas.draw()

    def destroy(self):
        print("SimplePlot destroy")
        if self.fig:
            plt.close(self.fig)
        super().destroy()   