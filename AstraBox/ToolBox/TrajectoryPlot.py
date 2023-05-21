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
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title(time_stamp)
        self.ax.axis('equal')
        self.ax.plot(self.plasma_bound['R'], self.plasma_bound['Z'])
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
        self.ax.plot(self.plasma_bound['R'], self.plasma_bound['Z'])
        for ray in rays:
            self.ax.plot(ray['R'], ray['Z'], alpha=0.5, linewidth=1)
        self.canvas.draw()

    def destroy(self):
        if self.fig:
            plt.close(self.fig)
        super().destroy()   