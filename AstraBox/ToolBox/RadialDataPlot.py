import json
import tkinter as tk
import tkinter
import tkinter.ttk as ttk
import AstraBox.WorkSpace as WorkSpace

from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import ( FigureCanvasTkAgg, NavigationToolbar2Tk)
from AstraBox.ToolBox.VerticalNavigationToolbar import VerticalNavigationToolbar2Tk
from AstraBox.Dialogs.PlotSettingDialog import PlotSettingDialog
import AstraBox.ToolBox.ImageButton as ImageButton

from AstraBox.Dialogs.Setting import PlotSetting, SubPlot

from rich import print 


class RadialDataPlot(ttk.Frame):
    def __init__(self, master, profiles) -> None:
        super().__init__(master)  
        self.data = profiles

        self.init_setting()

        self.fig = plt.figure(figsize=(8, 6.6))
        self.fig.suptitle(f'Astra radial data. Time={profiles["Time"]}')
        self.make_all_charts()

        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=1, rowspan= 2, sticky=tk.N + tk.S + tk.E + tk.W)

        tb = VerticalNavigationToolbar2Tk(self.canvas, self)
        tb.update()
        tb.grid(row=0, column=0, sticky=tk.N)
        
        btn = ImageButton.create(self, 'gear.png', self.option_windows)
        btn.grid(row=1, column=0, sticky=tk.N)        
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

    def init_setting(self):
        self.setting = PlotSetting.load('RadialPlot.setting')
        if self.setting is None:
            self.setting = PlotSetting(
            title= 'Radial Data',
            shape= '2x2',
            x_axis= 'rho',
            sub_plots= [
                SubPlot(name = 'ax1', title= 'профили токов', data= ['J', 'Johm', 'Jlh']), 
                SubPlot(name = 'ax2', title= 'профили E', data= ['E', 'En']), 
                SubPlot(name = 'ax3', title= 'профили мощности', data= ['Plh', 'Poh']), 
                SubPlot(name = 'ax4', title= 'профили температуры', data= ['Te'])
            ]
            )

        self.setting.x_axis_list.extend(['index', 'ameter', 'rho'])
        self.setting.data_terms.extend(self.data.keys())

        #print(self.setting)


    def option_windows(self):
        self.ps = PlotSettingDialog(self, self.setting, on_update_setting= self.on_update_setting )
        self.ps.show()


    def on_update_setting(self):
        print('on_update_setting')
        #print(self.setting)
        self.setting.save('RadialPlot.setting')
        for ax in self.axs.flat:
            ax.remove()
        self.make_all_charts()
        self.canvas.draw()    

    def get_x_axis_data(self):
        match self.setting.x_axis:
            case 'index': 
                return [i for i in range(len(self.data['a']))]
            case 'rho' :
                x_max= max(self.data['a']) 
                return [x/x_max for x in self.data['a']]
            case 'ameter':  
                return self.data['a']
    

    def make_all_charts(self):
            self.axs = self.fig.subplots(2, 2)  
            self.charts_list = {}
            x_axis_data = self.get_x_axis_data()
            sub_plots = self.setting.sub_plots
            for sub_plot, ax in zip(sub_plots, self.axs.flat):
                self.charts_list[sub_plot.name] = self.make_charts(ax, sub_plot, x_axis_data)
                ax.legend(loc='upper right')
                if self.setting.show_axis_labels:
                    ax.set_ylabel(sub_plot.y_label) 
                    ax.set_xlabel(self.setting.x_label)
                if self.setting.show_grid:
                    ax.grid(visible= True)
            #if self.setting.show_axis_labels:
            #    self.axs.flat[2].set_xlabel(self.setting.x_label)

    def make_charts(self, axis, sub_plot, x_axis_data):
        charts = {}
        terms = sub_plot.data
        for term in terms:
            if term in self.data.keys():
                chart, = axis.plot(x_axis_data, self.data[term], label= term)
                charts[term] = (chart)

        return charts

    def update(self, profiles):
        self.fig.suptitle(f'Astra radial data. Time={profiles["Time"]}')
        self.data = profiles
        sub_plots = self.setting.sub_plots
        for sub_plot in sub_plots:
            charts = self.charts_list[sub_plot.name]
            for key, chart in charts.items():
                chart.set_ydata(profiles[key]) 

        for ax in self.axs.flat:
            ax.relim()
            ax.autoscale_view(True,True,True)        

        self.canvas.draw()

    def destroy(self):
        if self.fig:
            plt.close(self.fig)
        super().destroy()   
