import tkinter as tk
import tkinter.ttk as ttk

from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import ( FigureCanvasTkAgg, NavigationToolbar2Tk)
from AstraBox.ToolBox.VerticalNavigationToolbar import VerticalNavigationToolbar2Tk
#from AstraBox.Dialogs.PlotSettingWindows import PlotSettingWindows
from AstraBox.Dialogs.PlotSettingDialog import PlotSettingDialog
import AstraBox.ToolBox.ImageButton as ImageButton

from AstraBox.Dialogs.Setting import PlotSetting, SubPlot

from rich import print 

class TimeSeriesPlot(ttk.Frame):
    def __init__(self, master, time_series) -> None:
        super().__init__(master)  
        self.fig = plt.figure(figsize=(10, 7), dpi=100)        
        self.data = time_series
        self.init_setting()
        self.make_all_charts()
        
        self.canvas = FigureCanvasTkAgg(self.fig, self)   
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=1, rowspan= 2, sticky=tk.N + tk.S + tk.E + tk.W)
        
        tb = VerticalNavigationToolbar2Tk(self.canvas, self)
        tb.update()
        tb.grid(row=0, column=0, sticky=tk.N)        

        btn = ImageButton.create(self, 'gear.png', self.show_option_windows)
        btn.grid(row=1, column=0, sticky=tk.N) 

        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)


    def init_setting(self):
        self.setting  = PlotSetting.load('TimeSeriesPlot.setting')
        if self.setting is None:
            self.setting = PlotSetting(
            title= 'Time Series',
            shape= '1x3',
            x_axis= 'time',
            x_label='time [ms]',
            sub_plots= [
                SubPlot(name = 'ax1', title= 'Chart 1', data= ['L']), 
                SubPlot(name = 'ax2', title= 'Chart 2', data= ['Iohm']), 
                SubPlot(name = 'ax3', title= 'Chart 3', data= ['V', 'Vexp']), 
            ]
            )

        self.setting.data_terms.extend(self.data.keys())


    def show_option_windows(self):
        ps = PlotSettingDialog(self, self.setting, on_update_setting= self.on_update_setting )
        ps.show()


    def on_update_setting(self):
        print('on_update_setting')
        self.setting.save('TimeSeriesPlot.setting')
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

        sub_plots = self.setting.sub_plots
        for sub_plot, ax in zip(sub_plots, self.axs.flat):
            self.charts_list[sub_plot.name] = self.make_charts(ax, sub_plot)
            ax.legend(loc='upper right')
            if self.setting.show_axis_labels:
                ax.set_ylabel(sub_plot.y_label) 
            if self.setting.show_grid:
                ax.grid(visible= True)
        if self.setting.show_axis_labels:
            self.axs.flat[2].set_xlabel(self.setting.x_label)
            

    def make_charts(self, axis, sub_plot):
        charts = {}
        terms = sub_plot.data
        for term in terms:
            if term in self.data.keys():
                chart, = axis.plot(self.data['Time'], self.data[term], label= term)
                charts[term] = (chart)

        return charts        