import tkinter as tk
import tkinter.ttk as ttk

from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import ( FigureCanvasTkAgg, NavigationToolbar2Tk)
from AstraBox.ToolBox.VerticalNavigationToolbar import VerticalNavigationToolbar2Tk


class DrivenCurrentPlot(ttk.Frame):
    def __init__(self, master, dc_series: dict) -> None:
        super().__init__(master)  
        keys = list(dc_series.keys())

        dc = [cup + cum for cup, cum in zip(dc_series['cup'], dc_series['cum'])]
        sigma = [cp0 + cm0 for cp0, cm0 in zip(dc_series['cp0'], dc_series['cm0'])]
        self.fig = plt.figure(figsize=(10, 8), dpi=100)        
        #self.fig.suptitle(f'Astra time series. ')
        gs = self.fig.add_gridspec(3, 1)

        ax1 = self.fig.add_subplot(gs[0, 0])
        ax1.plot(dc_series['Time'], dc_series[keys[2]], label=keys[1])
        ax1.plot(dc_series['Time'], dc_series[keys[2]], label=keys[2])
        ax1.plot(dc_series['Time'], dc_series[keys[3]], label=keys[3])
        ax1.plot(dc_series['Time'], dc_series[keys[4]], label=keys[4])
        ax1.plot(dc_series['Time'], dc, label='driven current')
        ax1.plot(dc_series['Time'], sigma, label='sigma dc')
        ax1.legend(loc='upper right', shadow=True)

        ax2 = self.fig.add_subplot(gs[1, 0])
        
        ax2.plot(dc_series['Time'], dc_series[keys[5]], label=keys[5])        
        ax2.plot(dc_series['Time'], dc_series[keys[6]], label=keys[6])
        ax2.legend(loc='upper right', shadow=True)

        ax3 = self.fig.add_subplot(gs[2, 0])
        ax3.plot(dc_series['Time'], dc_series[keys[7]], label=keys[7]) 
        ax3.plot(dc_series['Time'], dc_series[keys[8]], label=keys[8])
        ax3.legend(loc='upper right', shadow=True)

        ax1.set_ylabel('Current (MA)')
        ax2.set_ylabel('Current (MA)')
        ax3.set_ylabel('Current (MA)')        
        ax3.set_xlabel('Time')

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