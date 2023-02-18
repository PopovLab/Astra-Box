import tkinter as tk
import tkinter.ttk as ttk

from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import ( FigureCanvasTkAgg, NavigationToolbar2Tk)

class VerticalNavigationToolbar2Tk(NavigationToolbar2Tk):
   def __init__(self, canvas, window):
      super().__init__(canvas, window, pack_toolbar=False)

   # override _Button() to re-pack the toolbar button in vertical direction
   def _Button(self, text, image_file, toggle, command):
      b = super()._Button(text, image_file, toggle, command)
      b.pack(side=tk.TOP) # re-pack button in vertical direction
      return b

   # override _Spacer() to create vertical separator
   def _Spacer(self):
      s = tk.Frame(self, width=26, relief=tk.RIDGE, bg="DarkGray", padx=2)
      s.pack(side=tk.TOP, pady=5) # pack in vertical direction
      return s

   # disable showing mouse position in toolbar
   def set_message(self, s):
      pass


class RadialDataPlot(ttk.Frame):
    def __init__(self, master, profiles) -> None:
        super().__init__(master)  
        #self.fig, self.axs = plt.subplots(2, 2, figsize=(7, 6))
        self.fig = plt.figure(figsize=(8, 6.6))
        self.fig.suptitle(f'Astra radial data. Time={profiles["Time"]}')
        self.axs = self.fig.subplots(2, 2)
        
        # профили токов
        self.profile_J,    = self.axs[0,0].plot(profiles['a'], profiles['J'])
        self.profile_Johm, = self.axs[0,0].plot(profiles['a'], profiles['Johm'])
        self.profile_Jlh, = self.axs[0,0].plot(profiles['a'], profiles['Jlh'])
        self.axs[0,0].set_title("J, Johm, Jlh")

        # профили E
        self.profile_E, = self.axs[0,1].plot(profiles['a'], profiles['E'])
        self.profile_En, = self.axs[0,1].plot(profiles['a'], profiles['En'])
        self.axs[0,1].set_title("E, En")
    
        # профили мощности
        self.profile_Plh, = self.axs[1,0].plot(profiles['a'], profiles['Plh'])
        self.profile_Poh, = self.axs[1,0].plot(profiles['a'], profiles['Poh'])
        self.axs[1,0].set_title("Plh, Poh")
    
        # профили температуры
        self.profile_Te, = self.axs[1,1].plot(profiles['a'], profiles['Te'])
        #self.profile_Poh, = self.axs[2].plot(profiles['Poh'])
        self.axs[1,1].set_title("Te")

        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=1, sticky=tk.N + tk.S + tk.E + tk.W)

        #toobar = NavigationToolbar2Tk(self.canvas, frame)
        tb = VerticalNavigationToolbar2Tk(self.canvas, self)
        tb.update()
        tb.grid(row=0, column=0, sticky=tk.N)        
        
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

    def update(self, profiles):
        self.fig.suptitle(f'Astra radial data. Time={profiles["Time"]}')

        self.profile_J.set_ydata(profiles['J']) 
        self.profile_Johm.set_ydata(profiles['Johm']) 
        self.profile_Jlh.set_ydata(profiles['Jlh']) 
        self.axs[0,0].relim()
        self.axs[0,0].autoscale_view(True,True,True)        

        self.profile_E.set_ydata(profiles['E']) 
        self.profile_En.set_ydata(profiles['En']) 
        self.axs[0,1].relim()
        self.axs[0,1].autoscale_view(True,True,True) 

        self.profile_Plh.set_ydata(profiles['Plh']) 
        self.profile_Poh.set_ydata(profiles['Poh']) 
        self.axs[1,0].relim()
        self.axs[1,0].autoscale_view(True,True,True) 
        
        self.profile_Te.set_ydata(profiles['Te']) 
        self.axs[1,1].relim()
        self.axs[1,1].autoscale_view(True,True,True)         

        self.canvas.draw()

    def destroy(self):
        if self.fig:
            plt.close(self.fig)
        super().destroy()   



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
        self.canvas.get_tk_widget().grid(row=0, column=1)
        #toobar = NavigationToolbar2Tk(self.canvas, self, pack_toolbar=False)
        #toobar.grid(row=0, column=0, sticky=tk.W)
        tb = VerticalNavigationToolbar2Tk(self.canvas, self)
        tb.update()
        tb.grid(row=0, column=0, sticky=tk.N)    
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

    def update(self, rays, time_stamp):
        self.ax.clear()
        self.ax.set_title(time_stamp)
        self.ax.plot(self.R, self.Z)
        for ray in rays:
            self.ax.plot(ray['R'], ray['Z'], alpha=0.5, linewidth=1)
        self.canvas.draw()

    def destroy(self):
        if self.fig:
            plt.close(self.fig)
        super().destroy()   

#variable name
class RTResultPlot(ttk.Frame):
    def __init__(self, master, rt_result_dict, variable_name) -> None:
        super().__init__(master)  
        #self.fig, self.axs = plt.subplots(2, 2, figsize=(7, 6))
        self.rt_result_dict = rt_result_dict
        self.fig = plt.figure(figsize=(8, 5))
        self.fig.suptitle(f'RT Result. {variable_name}')
        self.ax1 = self.fig.subplots(1, 1)
        
        #  show rt result
        self.plot_data(variable_name, 1)
        self.plot_data(variable_name, -1)

        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=1, sticky=tk.N + tk.S + tk.E + tk.W)
        #toobar = NavigationToolbar2Tk(self.canvas, frame)
        tb = VerticalNavigationToolbar2Tk(self.canvas, self)
        tb.update()
        tb.grid(row=0, column=0, sticky=tk.N)    
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)    

    def plot_data(self, variable_name, direction):
        color = 'red'
        if direction>0: color = 'blue'
        X = []
        Y = []
        X0 = []
        Y0 = []
        for time_stamp, rt_result in self.rt_result_dict.items():
            iteration = 0
            for key, values in rt_result[direction].items():
                if key > iteration: iteration= key
                X.append(time_stamp)
                Y.append(values[variable_name])
            values = rt_result[direction][iteration]
            X0.append(time_stamp)
            Y0.append(values[variable_name])
        area = [3] * len(X)
        self.ax1.scatter(X, Y, s=area, c= color)
        self.ax1.plot(X0, Y0, c= color)

    def destroy(self):
        if self.fig:
            plt.close(self.fig)
        super().destroy()  

class DistributionPlot(ttk.Frame):
    def __init__(self, master, distribution, time_stamp) -> None:
        super().__init__(master)  
        #self.fig, self.axs = plt.subplots(2, 2, figsize=(7, 6))
        self.fig = plt.figure(figsize=(8, 5))
        self.fig.suptitle(f'Distribution. Time={time_stamp}')
        self.ax1 = self.fig.subplots(1, 1)
        
        #  show distribution
        for line in distribution:
            #self.ax1.plot(line['X'], line['Y'])
            self.ax1.plot(line['X'], line['logY']);


        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=1, sticky=tk.N + tk.S + tk.E + tk.W)
        #toobar = NavigationToolbar2Tk(self.canvas, frame)
        tb = VerticalNavigationToolbar2Tk(self.canvas, self)
        tb.update()
        tb.grid(row=0, column=0, sticky=tk.N)    
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)        

    def update(self, distribution, time_stamp):
        self.fig.suptitle(f'Distribution. Time={time_stamp}')
        self.ax1.clear()
        for line in distribution:
            #self.ax1.plot(line['X'], line['Y'])
            self.ax1.plot(line['X'], line['logY']);

        self.ax1.set_ylim(-30, 0)
        #self.ax1.autoscale_view(True,True,True)        

        self.canvas.draw()

    def destroy(self):
        if self.fig:
            plt.close(self.fig)
        super().destroy()   

class SeriesPlot(ttk.Frame):
    def __init__(self, master, series, title, time_stamp, уscale_log = True) -> None:
        super().__init__(master)  
        self.уscale_log = уscale_log
        self.title = title
        self.series = series

        tb = self.make_toolbar()
        tb.grid(row=0, column=0, columnspan=2, sticky=tk.N + tk.S + tk.E + tk.W) 

        self.fig = plt.figure(figsize=(8, 5))
        self.fig.suptitle(f'{self.title} Time={time_stamp}')
        self.ax1 = self.fig.subplots(1, 1)

        #  show distribution
        for item in series:
            self.ax1.plot(item['X'], item['Y']);

        if self.уscale_log:
            self.ax1.set_yscale('log')

        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=1, column=1, sticky=tk.N + tk.S + tk.E + tk.W)
        #toobar = NavigationToolbar2Tk(self.canvas, frame)
        tb = VerticalNavigationToolbar2Tk(self.canvas, self)
        tb.update()
        tb.grid(row=1, column=0, sticky=tk.N)    
        self.columnconfigure(1, weight=1)
        #self.rowconfigure(0, weight=1)        
        self.rowconfigure(1, weight=1)

    def make_toolbar(self):
        frame = ttk.Frame(self)
  
        self.chk_var = tk.IntVar(master = self, value=self.уscale_log)
  
        self.checkbtn = ttk.Checkbutton(master=  frame, text="Log scale", variable=self.chk_var, command=self.checkbtn_changed )
        self.checkbtn.pack(side=tk.LEFT, expand=1, fill=tk.X, padx=5) 
        ns= len(self.series)
        self.index_1 = tk.IntVar(master = self, value=0)
        self.index_1.trace_add('write', self.update_plot)
        self.slider_1 = tk.Scale(master=  frame, variable = self.index_1, orient = tk.HORIZONTAL, 
                                    sliderlength = 20,
                                    width = 10,            
                                    label='index',
                                    tickinterval= ns/4,
                                    from_=0, 
                                    to=ns-1, 
                                    resolution=1 )
        self.slider_1.pack(side=tk.LEFT, expand=1, fill=tk.X, padx=5) 

        self.index_2 = tk.IntVar(master = self, value=ns)
        self.index_2.trace_add('write', self.update_plot)
        self.slider_2 = tk.Scale(master=  frame, variable = self.index_2, orient = tk.HORIZONTAL,
                                    sliderlength = 20,
                                    width = 10,            
                                    label='numbers',
                                    tickinterval= ns/4,
                                    from_=1, 
                                    to=ns, 
                                    resolution=1 )
        self.slider_2.pack(side=tk.LEFT, expand=1, fill=tk.X, padx=5)   
            
        return frame
        
    def checkbtn_changed(self):
        if self.chk_var.get() == 1:
            self.уscale_log = True
        else:
            self.уscale_log = False
        self.show_series(save_lim = False) 

    def update_plot(self, var, indx, mode):
        self.show_series()

    def update(self, series, time_stamp):
        self.series = series
        self.fig.suptitle(f'{self.title}. Time={time_stamp}')
        self.show_series()

    def show_series(self, save_lim = True):
        if save_lim:
            bottom, top = self.ax1.get_ylim()
            left, right = self.ax1.get_xlim()        
        self.ax1.clear()
        i1 = self.index_1.get()
        i2 = i1 + self.index_2.get()
        if i2>len(self.series):
            i2 = len(self.series)
        print(f'{i1} {i2}')
        for item in self.series[i1:i2]:
            self.ax1.plot(item['X'], item['Y']);
        if self.уscale_log:
            self.ax1.set_yscale('log')
        if save_lim:
            self.ax1.set_ylim(bottom, top)
            self.ax1.set_xlim(left, right)            
        self.canvas.draw()

    def destroy(self):
        if self.fig:
            plt.close(self.fig)
        super().destroy()                   