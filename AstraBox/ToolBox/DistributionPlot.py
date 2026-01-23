import tkinter as tk
import tkinter.ttk as ttk

from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from AstraBox.ToolBox.VerticalNavigationToolbar import VerticalNavigationToolbar2Tk


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