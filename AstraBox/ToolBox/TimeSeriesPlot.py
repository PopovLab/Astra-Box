import tkinter as tk
import tkinter.ttk as ttk

from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import ( FigureCanvasTkAgg, NavigationToolbar2Tk)
from AstraBox.ToolBox.VerticalNavigationToolbar import VerticalNavigationToolbar2Tk


class TimeSeriesPlot(ttk.Frame):
    def __init__(self, master, time_series, keys) -> None:
        super().__init__(master)  
        self.fig = plt.figure(figsize=(10, 7), dpi=100)        
        #self.fig.suptitle(f'Astra time series. ')
        gs = self.fig.add_gridspec(3, 1)

        ax1 = self.fig.add_subplot(gs[0, 0])
        ax1.plot(time_series['Time'], time_series[keys[0]], label=keys[0])
        ax1.legend(loc='upper right', shadow=True)

        ax2 = self.fig.add_subplot(gs[1, 0])
        ax2.plot(time_series['Time'], time_series[keys[1]], label=keys[1])
        ax2.legend(loc='upper right', shadow=True)

        ax3 = self.fig.add_subplot(gs[2, 0])
        ax3.plot(time_series['Time'], time_series[keys[2]], label=keys[2])
        ax3.legend(loc='upper right', shadow=True)

        ax3.set_xlabel('Time')
        ax1.set_ylabel(keys[0])
        ax2.set_ylabel(keys[1])
        ax3.set_ylabel(keys[2])

        self.canvas = FigureCanvasTkAgg(self.fig, self)   
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=1)
        tb = VerticalNavigationToolbar2Tk(self.canvas, self)
        tb.update()
        tb.grid(row=0, column=0, sticky=tk.N)        

        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

    def destroy(self):
        print("TimeSeriesPlot destroy")
        if self.fig:
            plt.close(self.fig)
        super().destroy()   