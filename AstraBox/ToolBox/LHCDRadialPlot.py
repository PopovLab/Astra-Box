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


class LHCDRadialPlot(ttk.Frame):
    def __init__(self, master, data) -> None:
        super().__init__(master)  
        self.data = data
        
        #self.ps = PlotSettingDialog(self, 
        #                             terms= profiles.keys(), 
        #                             file_name= 'RadialPlotSetting.json', 
        #                             default_data= default_radial_setting(),
        #                             on_update_setting= self.on_update_setting )
        self.fig = plt.figure(figsize=(8, 6.6))
        self.fig.suptitle(f'LHCD Radial data. Time={data["pos"]["Time"]}')
        
        self.ax = self.fig.add_subplot(111)
        self.make_plots()
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
        #self.ps.show()
        pass

    def make_plots(self):
        self.ax.clear()
        self.ax.plot(self.data['pos']['Data']['index'], self.data['pos']['Data']['pdl'], c= 'darkred', label= 'pos pdl')
        self.ax.plot(self.data['neg']['Data']['index'], self.data['neg']['Data']['pdl'], c= 'blue', label= 'neg pdl')
        self.ax.plot(self.data['pos']['Data']['index'], self.data['pos']['Data']['pdc'], c= 'salmon', label= 'pos pdc')
        self.ax.plot(self.data['neg']['Data']['index'], self.data['neg']['Data']['pdc'], c= 'violet', label= 'neg pdc')        
        self.ax.legend(loc='upper right')

    def update(self, data):
        self.fig.suptitle(f'LHCD Radial data. Time={data["pos"]["Time"]}')
        self.data = data
        self.make_plots()
        self.canvas.draw()

    def destroy(self):
        if self.fig:
            plt.close(self.fig)
        super().destroy()   
