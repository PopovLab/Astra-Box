import json
import tkinter as tk
import tkinter
import tkinter.ttk as ttk
import AstraBox.WorkSpace as WorkSpace

from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import ( FigureCanvasTkAgg, NavigationToolbar2Tk)
from AstraBox.ToolBox.VerticalNavigationToolbar import VerticalNavigationToolbar2Tk
from AstraBox.Views.PlotSettingDialog import PlotSettingDialog
import AstraBox.ToolBox.ImageButton as ImageButton

def default_radial_setting():
    # настройки по умолчанию для рейтрейсинга
    # профили токов
    # профили E
    # профили мощности
    # профили температуры  
    return {
        'shape' : '2x2',
        'title' : 'Radial Data setting',
        'plots'  : {
            'ax1' : ['J', 'Johm', 'Jlh'],
            'ax2' : ['E', 'En'],
            'ax3' : ['Plh', 'Poh'],
            'ax4' : ['Te']
            }
        }


class RadialDataPlot(ttk.Frame):
    def __init__(self, master, profiles) -> None:
        super().__init__(master)  
        self.data = profiles
        #self.fig, self.axs = plt.subplots(2, 2, figsize=(7, 6))
        self.ps = PlotSettingDialog(self, 
                                     terms= profiles.keys(), 
                                     file_name= 'RadialPlotSetting.json', 
                                     default_data= default_radial_setting(),
                                     on_update_setting= self.on_update_setting )
        self.fig = plt.figure(figsize=(8, 6.6))
        self.fig.suptitle(f'Astra radial data. Time={profiles["Time"]}')
        self.make_all_charts()

        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=1, rowspan= 2, sticky=tk.N + tk.S + tk.E + tk.W)

        #toobar = NavigationToolbar2Tk(self.canvas, frame)
        tb = VerticalNavigationToolbar2Tk(self.canvas, self)
        tb.update()
        tb.grid(row=0, column=0, sticky=tk.N)
        
        #btn = ttk.Button(self, text= 'Q', width= 2, command= self.option_windows )
        btn = ImageButton.create(self, 'gear.png', self.option_windows)
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


    def make_all_charts(self):
            self.axs = self.fig.subplots(2, 2)  
            self.charts_list = {}
      
            plots = self.ps.data['plots']
            for (key, terms), ax in zip(plots.items(), self.axs.flat):
                self.charts_list[key] = self.make_charts(ax, key)
                ax.legend(loc='upper right')

    def make_charts(self, axis, plot_name):
        charts = {}
        terms = self.ps.data['plots'][plot_name]
        for term in terms:
            if term in self.data.keys():
                chart, = axis.plot(self.data['a'], self.data[term], label= term)
                charts[term] = (chart)

        return charts

    def update(self, profiles):
        self.fig.suptitle(f'Astra radial data. Time={profiles["Time"]}')
        self.data = profiles
        plots = self.ps.data['plots']
        for key, terms in plots.items():
            charts = self.charts_list[key]
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
