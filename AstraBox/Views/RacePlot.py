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
        #canvas.get_tk_widget().grid(row=2, column=0)

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



class DistributionPlot(ttk.Frame):
    def __init__(self, master, distribution, time_stamp) -> None:
        super().__init__(master)  
        #self.fig, self.axs = plt.subplots(2, 2, figsize=(7, 6))
        self.fig = plt.figure(figsize=(8, 5))
        self.fig.suptitle(f'Distribution. Time={time_stamp}')
        self.ax1 = self.fig.subplots(1, 1)
        
        # 
        for line in distribution:
            #self.ax1.plot(line['X'], line['Y'])
            self.ax1.plot(line['X'], line['logY']);


        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=1, sticky=tk.N + tk.S + tk.E + tk.W)
        #frame = ttk.Frame(self)
        #frame.grid(row=0, column=0, sticky=tk.W)
        #toobar = NavigationToolbar2Tk(self.canvas, frame)
        tb = VerticalNavigationToolbar2Tk(self.canvas, self)
        tb.update()
        tb.grid(row=0, column=0, sticky=tk.N)    

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