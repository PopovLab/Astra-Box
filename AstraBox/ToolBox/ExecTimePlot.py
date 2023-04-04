import tkinter as tk
import tkinter.ttk as ttk

from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import ( FigureCanvasTkAgg, NavigationToolbar2Tk)
from AstraBox.ToolBox.VerticalNavigationToolbar import VerticalNavigationToolbar2Tk


class ExecTimePlot(ttk.Frame):
    def __init__(self, master, data_series: dict) -> None:
        super().__init__(master)  
        keys = list(data_series.keys())

        self.fig = plt.figure(figsize=(10, 8), dpi=100)        
        #self.fig.suptitle(f'Astra time series. ')
        gs = self.fig.add_gridspec(1, 1)

        ax1 = self.fig.add_subplot(gs[0, 0])
        ax1.plot(data_series[keys[0]]['X'],data_series[keys[0]]['Y'], label=keys[0])
        ax1.plot(data_series[keys[1]]['X'],data_series[keys[1]]['Y'], label=keys[1])
        

        ax1.legend(loc='upper right')

        ax1.set_ylabel('CPU time')

        ax1.set_xlabel('Plasma time (sec)')

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