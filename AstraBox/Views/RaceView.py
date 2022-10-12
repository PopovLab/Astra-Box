import tkinter as tk
import tkinter.ttk as ttk

from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import ( FigureCanvasTkAgg, NavigationToolbar2Tk)

from AstraBox.Views.HeaderPanel import HeaderPanel
import AstraBox.Models.ModelFactory as ModelFactory

class RaceView(ttk.Frame):
 
    def __init__(self, master, model) -> None:
        super().__init__(master)        
        #self.title = 'ImpedModelView'
        title = f"Race data View {model.name}"
        print(title)
        self.header_content = { "title": title, "buttons":[('Save', None), ('Delete', self.delete_model)]}
        self.model = model
        self.hp = HeaderPanel(self, self.header_content)
        self.hp.grid(row=0, column=0, columnspan=5, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)
        self.columnconfigure(0, weight=1)        
        #self.rowconfigure(0, weight=1)    

        #self.InitUI(model)

        self.label = ttk.Label(self,  text=f'zip file:{model.race_zip_file}')
        self.label.grid(row=1, column=0, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W)        

        self.radial_data_list = model.get_radial_data_list()

        if len(self.radial_data_list)>0: 
            self.index_var = tk.IntVar(master = self, value=0)
            self.index_var.trace_add('write', self.update_var)

            self.slider = tk.Scale(master=  self, variable = self.index_var, orient = tk.HORIZONTAL, from_=0, to=len(self.radial_data_list)-1, resolution=1, length = 250 )
            self.slider.grid(row=2, column=0, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W)       
 
            profiles = self.get_profiles(0)
            self.plot = SimplePlot(self, profiles)
            self.plot.grid(row=4, column=0, sticky=tk.W, pady=4, padx=8)

    def delete_model(self):
        ModelFactory.delete_model(self.model)

    def get_profiles(self, index):
        file = self.radial_data_list[index]
        print(f'{file} {index}')
        return self.model.read_radial_data(file)

    def update_var(self, var, indx, mode):
        profiles = self.get_profiles(self.index_var.get())
        self.plot.update(profiles)
        
    def destroy(self):
        print("RaceView destroy")
        super().destroy()   

class SimplePlot(ttk.Frame):
    def __init__(self, master, profiles) -> None:
        super().__init__(master)  
        #self.fig, self.axs = plt.subplots(2, 2, figsize=(7, 6))
        self.fig = plt.figure(figsize=(7, 6))
        self.fig.suptitle(f'Astra radial data. Time={profiles["Time"]}')
        self.axs = self.fig.subplots(2, 2)
        self.profile_a, = self.axs[0,0].plot(profiles['a'])
        #axs[0,0].plot(profiles2['a'])    
        self.axs[0,0].set_title("a")

        self.profile_J, = self.axs[1,0].plot(profiles['J'])
        #axs[1,0].plot(profiles2['J'])
        self.axs[1,0].set_title("J")

        self.profile_E, = self.axs[0,1].plot(profiles['E'])
        self.axs[0,1].set_title("E")
    
        self.profile_Johm, = self.axs[1,1].plot(profiles['Johm'])
        self.axs[1,1].set_title("Johm")

        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=1, column=0)
        frame = ttk.Frame(self)
        frame.grid(row=0, column=0, sticky=tk.W)
        toobar = NavigationToolbar2Tk(self.canvas, frame)
        #tb = VerticalNavigationToolbar2Tk(canvas, frame)
        #canvas.get_tk_widget().grid(row=2, column=0)

    def update(self, profiles):
        self.fig.suptitle(f'Astra radial data. Time={profiles["Time"]}')

        #self.profile_a.set_xdata([1,2,3,5])
        self.profile_a.set_ydata(profiles['a']) 
        self.axs[0,0].relim()
        self.axs[0,0].autoscale_view(True,True,True)        
        
        self.profile_J.set_ydata(profiles['J']) 
        self.axs[1,0].relim()
        self.axs[1,0].autoscale_view(True,True,True)   

        self.profile_E.set_ydata(profiles['E']) 
        self.axs[0,1].relim()
        self.axs[0,1].autoscale_view(True,True,True) 

        self.profile_Johm.set_ydata(profiles['Johm']) 
        self.axs[1,1].relim()
        self.axs[1,1].autoscale_view(True,True,True)  

        self.canvas.draw()

    def destroy(self):
        print("SimplePlot destroy")
        if self.fig:
            plt.close(self.fig)
        super().destroy()   