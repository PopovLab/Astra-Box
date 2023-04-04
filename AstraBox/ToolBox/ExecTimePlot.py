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

        self.fig = plt.figure(figsize=(9, 5), dpi=100)        
        #self.fig.suptitle(f'Astra time series. ')

        ax = self.fig.add_subplot(111)
        ax.plot(data_series[keys[0]]['X'],data_series[keys[0]]['Y'], label=keys[0])
        ax.plot(data_series[keys[1]]['X'],data_series[keys[1]]['Y'], label=keys[1])
        

        ax.legend(loc='upper right')
        ax.set_ylabel('System time')
        ax.set_xlabel('Plasma time (sec)')

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