import tkinter as tk
import tkinter.ttk as ttk

from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import ( FigureCanvasTkAgg, NavigationToolbar2Tk)
from AstraBox.ToolBox.VerticalNavigationToolbar import VerticalNavigationToolbar2Tk
from AstraBox.Views.PlotSettingWindows import PlotSettingWindows

def default_time_plot_setting():
    return {
        'shape' : '1x3',
        'title' : 'Time Series data',
        'plots'  : {
            'ax1' : ['L'],
            'ax2' : ['Iohm'],
            'ax3' : ['V', 'Vexp'],
            }
        }

class TimeSeriesPlot(ttk.Frame):
    def __init__(self, master, time_series) -> None:
        super().__init__(master)  
        self.fig = plt.figure(figsize=(10, 7), dpi=100)        
        #self.fig.suptitle(f'Astra time series. ')
        self.data = time_series
        self.ps = PlotSettingWindows(self, 
                                     terms= time_series.keys(), 
                                     file_name= 'TimeSeriesPlotSetting.json', 
                                     default_data= default_time_plot_setting(),
                                     on_update_setting= self.on_update_setting )
                
        self.make_all_charts()

        self.canvas = FigureCanvasTkAgg(self.fig, self)   
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=1, rowspan=2)
        tb = VerticalNavigationToolbar2Tk(self.canvas, self)
        tb.update()
        tb.grid(row=0, column=0, sticky=tk.N)        

        btn = ttk.Button(self, text= 'Q', width= 2, command= self.option_windows )
        btn.grid(row=1, column=0, sticky=tk.N) 

        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

    def option_windows(self):
        self.ps.show()

    def on_update_setting(self):
        print('on_update_setting')
        print(self.ps.data['plots'])
        for ax in self.axs.flat:
            ax.remove()
        self.make_all_charts()
        self.canvas.draw() 

    def destroy(self):
        print("TimeSeriesPlot destroy")
        if self.fig:
            plt.close(self.fig)
        super().destroy()   


    def make_all_charts(self):
        self.axs = self.fig.subplots(3, 1)  
        self.charts_list = {}
    
        plots = self.ps.data['plots']
        for (key, terms), ax in zip(plots.items(), self.axs.flat):
            self.charts_list[key] = self.make_charts(ax, key)
            ax.legend(loc='upper right')

        self.axs.flat[2].set_xlabel('Time')
        #ax1.set_ylabel(keys[0])
        #ax2.set_ylabel(keys[1])
        #ax3.set_ylabel("V")                

    def make_charts(self, axis, plot_name):
        charts = {}
        terms = self.ps.data['plots'][plot_name]
        for term in terms:
            if term in self.data.keys():
                chart, = axis.plot(self.data['Time'], self.data[term], label= term)
                charts[term] = (chart)

        return charts        