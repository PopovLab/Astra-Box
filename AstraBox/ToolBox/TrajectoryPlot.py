import tkinter as tk
import tkinter.ttk as ttk

from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import ( FigureCanvasTkAgg, NavigationToolbar2Tk)
from AstraBox.ToolBox.VerticalNavigationToolbar import VerticalNavigationToolbar2Tk


class TrajectoryPlot(ttk.Frame):
    def __init__(self, master, rays, time_stamp, plasma_bound) -> None:
        super().__init__(master)  
        self.plasma_bound = plasma_bound
        self.fig = plt.figure(figsize=(6,6))
        #self.fig.title(time_stamp)
        self.ax1, self.ax2 = self.fig.subplots(2, 1)
        self.ax1.set_title(time_stamp, fontsize=12)
        self.ax1.axis('equal')
        self.ax1.plot(self.plasma_bound['R'], self.plasma_bound['Z'])
        for ray in rays:
            self.ax1.plot(ray['R'], ray['Z'], alpha=0.5, linewidth=0.5)

        self.ax2.set_title('N_par', fontsize=12)
        self.ax2.set_xlabel('theta', fontsize=12)
        for ray in rays:
            self.ax2.plot(ray['theta'], ray['N_par'], alpha=0.5, linewidth=0.5)

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
        self.ax1.clear()
        self.ax1.set_title(time_stamp, fontsize=12)
        self.ax1.plot(self.plasma_bound['R'], self.plasma_bound['Z'])
        for ray in rays:
            self.ax1.plot(ray['R'], ray['Z'], alpha=0.5, linewidth=0.5)
        
        self.ax2.clear()
        self.ax2.set_title('N_par', fontsize=12)
        self.ax2.set_xlabel('theta', fontsize=12)
        for ray in rays:
            #print(ray)
            #self.ax2.plot(ray['N_par'], alpha=0.5, linewidth=0.5)   
            self.ax2.plot(ray['theta'], ray['N_par'], alpha=0.5, linewidth=0.5)         
        self.canvas.draw()

    def destroy(self):
        if self.fig:
            plt.close(self.fig)
        super().destroy()   