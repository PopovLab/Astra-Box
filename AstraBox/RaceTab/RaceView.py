#from cgitb import enable
import tkinter as tk
import tkinter.ttk as ttk
from typing import Any
import tkinter.messagebox as messagebox
import pandas as pd
from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import ( FigureCanvasTkAgg, NavigationToolbar2Tk)

from AstraBox.RaceTab.TabViewBasic import TabViewBasic
import AstraBox.WorkSpace as WorkSpace
import AstraBox.Models.ModelFactory as ModelFactory

from AstraBox.Views.HeaderPanel import HeaderPanel
from AstraBox.Views.ExtraRaceView import ExtraRaceView


from AstraBox.Models.RaceModel import RaceModel

from AstraBox.ToolBox.ComboBox import ComboBox
from AstraBox.ToolBox.RadialDataPlot import RadialDataPlot
from AstraBox.ToolBox.TimeSeriesPlot import TimeSeriesPlot
from AstraBox.ToolBox.RadialDataPlot import RadialDataPlot
from AstraBox.ToolBox.TrajectoryPlot import TrajectoryPlot
from AstraBox.ToolBox.DistributionPlot import DistributionPlot
from AstraBox.ToolBox.SeriesPlot import SeriesPlot
from AstraBox.ToolBox.RTResultPlot import RTResultPlot
from AstraBox.ToolBox.DrivenCurrentPlot import DrivenCurrentPlot
from AstraBox.RaceTab.LHCDRadialPlot import LHCDRadialPlot
from AstraBox.ToolBox.MaxwellPlot import MaxwellPlot
from AstraBox.ToolBox.ExecTimePlot import ExecTimePlot
from AstraBox.ToolBox.RadialDCPlot import RadialDCPlot

           



from statistics import mean 
from statistics import stdev
class ExecTimeView(TabViewBasic):
    def __init__(self, master, model: RaceModel) -> None:
        super().__init__(master, model)  

    def init_ui(self):
        print('init Exec Time View')
        self.data_series = self.race_model.get_exec_time()
        if type(self.data_series) == dict:
            self.make_plot()
        else:
            label = tk.Label(master=self, text=self.data_series)
            label.grid(row=0, column=1, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)	            

    def make_plot(self):
        #keys = [self.combo1.get(), self.combo2.get(), self.combo3.get()]
        self.plot = ExecTimePlot(self, self.data_series )
        self.plot.grid(row=1, column=0, padx=4, sticky=tk.N + tk.S + tk.E + tk.W)

        text_box = tk.Text(self, height = 10, width = 20)
        text_box.grid(row=2, column=0, padx=4, pady=4, sticky=tk.N + tk.S + tk.E + tk.W)
        self.add_text(text_box)
        text_box.config(state='disabled')

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

    def add_text(self, text_box):
        lines = ['Summary:']
        
        for key, data in self.data_series.items():
            indent = ' ' * 2
            lines.append(indent + key)
            indent = ' ' * 4 
            lines.append(indent + f'  sum time: {sum(data["Y"])} ')
            lines.append(indent + f'mean  time: {mean(data["Y"])} ')
            lines.append(indent + f'stdev time: {stdev(data["Y"])} ')

        text_box.insert(tk.END, '\n'.join(lines))


class DrivenCurrentView(TabViewBasic):
    def __init__(self, master, model: RaceModel) -> None:
        super().__init__(master, model)  

    def init_ui(self):
        print('init Time Series View')
        self.data_frame = self.race_model.get_driven_current()
        if type(self.data_frame) == pd.DataFrame:
            self.make_plot()
        else:
            label = tk.Label(master=self, text=self.data_frame)
            label.grid(row=0, column=1, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)	            

    def make_plot(self):
        #keys = [self.combo1.get(), self.combo2.get(), self.combo3.get()]
        self.plot = DrivenCurrentPlot(self, self.data_frame )
        self.plot.grid(row=1, column=0, columnspan=3, padx=4, sticky=tk.N + tk.S + tk.E + tk.W)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

class TimeSeriesView(TabViewBasic):
    def __init__(self, master, model: RaceModel) -> None:
        super().__init__(master, model)  

    def init_ui(self):
        print('init Time Series View')
        self.time_series = self.race_model.get_time_series()
        if type(self.time_series) == pd.core.frame.DataFrame:
            self.plot = TimeSeriesPlot(self, self.time_series)
            self.plot.grid(row=1, column=0, columnspan=3, padx=4, sticky=tk.N + tk.S + tk.E + tk.W)
            self.columnconfigure(1, weight=1)
            self.rowconfigure(1, weight=1)
        else:
            label = tk.Label(master=self, text=self.time_series)
            label.grid(row=0, column=1, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)	
        

class RTResultView(TabViewBasic):
    def __init__(self, master, model: RaceModel) -> None:
        super().__init__(master, model)  

    def init_ui(self):
        print('init RT result View')
        self.rt_result_file_list = self.race_model.get_file_list('RT_RESULT')
        self.rt_result_dict = {}
        n = len(self.rt_result_file_list)
        if n>0: 
            start_time = 100 
            finish_time = 0
            keys = []

            for f in self.rt_result_file_list:
                time_stamp, rt_result, keys = self.race_model.get_rt_result(f)
                self.rt_result_dict[time_stamp] = rt_result
                if time_stamp>finish_time: finish_time = time_stamp
                if time_stamp<start_time: start_time = time_stamp

            self.combo1 = ComboBox(self, 'View 1', keys)
            self.combo1.grid(row=0, column=0, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)
            self.combo2 = ComboBox(self, 'View 2', keys)
            self.combo2.grid(row=0, column=1, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)            
 
            self.combo1.set(keys[3])
            self.combo2.set(keys[4])

            self.combo1.on_combo_selected = self.show_rt_result
            self.combo2.on_combo_selected = self.show_rt_result
            self.show_rt_result()
        else:
            label = tk.Label(master=self, text='Нет данных')
            label.grid(row=0, column=1, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)	

    def show_rt_result(self):
        keys = [self.combo1.get(), self.combo2.get()]
        print(f'show_rt_result: {keys}')
        self.plot = RTResultPlot(self,self.rt_result_dict, keys)
        self.plot.grid(row=1, column=0, columnspan=3, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)


class RadialDrivenCurrentView(TabViewBasic):
    def __init__(self, master, model: RaceModel) -> None:
        super().__init__(master, model)  

    def init_ui(self):   
        self.dc_list = self.race_model.get_file_list('DC')
        n = len(self.dc_list)
        print(f'n= {n}')
        if n>0: 
            dc_data = self.get_dc_data(0)
            self.start_time = dc_data["Time"]
            self.finish_time = self.get_dc_data(n-1)["Time"]
            print(f'{self.start_time} - {self.finish_time}')
            self.n = n
            
            self.time_var = tk.DoubleVar(master = self, value=self.start_time)
            self.time_var.trace_add('write', self.update_time_var)

            self.time_slider = tk.Scale(master=  self, 
                                   variable = self.time_var,
                                   orient = tk.HORIZONTAL,
                                   label='Time scale',
                                   tickinterval= (self.finish_time-self.start_time)/7,
                                   from_= self.start_time,
                                   to= self.finish_time, 
                                   resolution= (self.finish_time-self.start_time)/n, 
                                   length = 250 )
            self.time_slider.grid(row=1, column=0, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W)       
            
            self.plot = RadialDCPlot(self, dc_data)
            self.plot.grid(row=2, column=0, sticky=tk.N + tk.S + tk.E + tk.W, pady=4, padx=8)
            self.columnconfigure(0, weight=1)
            self.rowconfigure(2, weight=1)
        else:
            label = tk.Label(master=self, text='Нет данных')
            label.grid(row=0, column=1, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)

    def get_dc_data(self, index):
        file = self.dc_list[index]
        print(f'{file} {index}')
        return self.race_model.read_dc_data(file)

    def update_time_var(self, var, indx, mode):
        index = int((self.n-1) * (self.time_var.get()-self.start_time) / (self.finish_time-self.start_time))
        dc_data = self.get_dc_data(index)
        self.plot.update(dc_data)

    def update_var(self, var, indx, mode):
        radial_data = self.get_dc_data(self.index_var.get())
        #self.plot.update(radial_data)

class RadialDataView(TabViewBasic):
    def __init__(self, master, model: RaceModel) -> None:
        super().__init__(master, model)  

    def init_ui(self):   
        self.radial_data_list = self.race_model.get_file_list('RADIAL_DATA')
        n = len(self.radial_data_list)
        print(f'n= {n}')
        if n>0: 
            radial_data = self.get_radial_data(0)
            self.start_time = radial_data["Time"]
            self.finish_time = self.get_radial_data(n-1)["Time"]
            print(f'{self.start_time} - {self.finish_time}')
            self.n = n
            
            self.time_var = tk.DoubleVar(master = self, value=self.start_time)
            self.time_var.trace_add('write', self.update_time_var)

            self.time_slider = tk.Scale(master=  self, 
                                   variable = self.time_var,
                                   orient = tk.HORIZONTAL,
                                   label='Time scale',
                                   tickinterval= (self.finish_time-self.start_time)/7,
                                   from_= self.start_time,
                                   to= self.finish_time, 
                                   resolution= (self.finish_time-self.start_time)/n, 
                                   length = 250 )
            self.time_slider.grid(row=1, column=0, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W)       
            
            self.plot = RadialDataPlot(self, radial_data)
            self.plot.grid(row=2, column=0, sticky=tk.N + tk.S + tk.E + tk.W, pady=4, padx=8)
            self.columnconfigure(0, weight=1)
            self.rowconfigure(2, weight=1)
        else:
            label = tk.Label(master=self, text='Нет данных')
            label.grid(row=0, column=1, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)

    def get_radial_data(self, index):
        file = self.radial_data_list[index]
        print(f'{file} {index}')
        return self.race_model.read_radial_data(file)

    def update_time_var(self, var, indx, mode):
        index = int((self.n-1) * (self.time_var.get()-self.start_time) / (self.finish_time-self.start_time))
        radial_data = self.get_radial_data(index)
        self.plot.update(radial_data)

    def update_var(self, var, indx, mode):
        radial_data = self.get_radial_data(self.index_var.get())
        self.plot.update(radial_data)


class DistributionView(TabViewBasic):
    def __init__(self, master, model: RaceModel) -> None:
        super().__init__(master, model)  

    def init_ui(self):   
        self.distribution_list = self.race_model.get_file_list('DISTRIBUTION') 
        n = len(self.distribution_list)
        if n>0: 
            distribution, self.start_time  =  self.get_distribution(0)
            _, self.finish_time  = self.get_distribution(n-1)
            self.n = n

            self.time_var = tk.DoubleVar(master = self, value=self.start_time)
            self.time_var.trace_add('write', self.update_time_var)

            self.time_slider = tk.Scale(master=  self, 
                                   variable = self.time_var,
                                   orient = tk.HORIZONTAL,
                                   label='Time scale',
                                   tickinterval= (self.finish_time-self.start_time)/7,
                                   from_= self.start_time,
                                   to= self.finish_time, 
                                   resolution= (self.finish_time-self.start_time)/n, 
                                   length = 250 )
            self.time_slider.grid(row=1, column=0, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W)       
            
            self.plot = DistributionPlot(self, distribution, self.start_time)
            self.plot.grid(row=2, column=0, sticky=tk.N + tk.S + tk.E + tk.W, pady=4, padx=8)
            self.columnconfigure(0, weight=1)
            self.rowconfigure(2, weight=1)            
        else:
            label = tk.Label(master=self, text='Нет данных')
            label.grid(row=0, column=1, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)            

    def get_distribution(self, index):
        file = self.distribution_list[index]
        print(f'{file} {index}')
        return self.race_model.read_distribution(file)

    def update_time_var(self, var, indx, mode):
        index = int((self.n-1) * (self.time_var.get()-self.start_time) / (self.finish_time-self.start_time))
        distribution, time_stamp = self.get_distribution(index)
        self.plot.update(distribution, time_stamp)

    def update_var(self, var, indx, mode):
        distribution, time_stamp  = self.get_distribution(self.index_var.get())
        self.plot.update(distribution)


class MaxwellView(TabViewBasic):
    def __init__(self, master, model: RaceModel) -> None:
        super().__init__(master, model)  

    def init_ui(self): 
        self.maxwell_list = self.race_model.get_file_list('MAXWELL')
        n = len(self.maxwell_list)
        if n>0: 
            distribution, self.start_time  =  self.get_distribution(0)
            _, self.finish_time  = self.get_distribution(n-1)
            self.n = n

            self.time_var = tk.DoubleVar(master = self, value=self.start_time)
            self.time_var.trace_add('write', self.update_time_var)

            self.time_slider = tk.Scale(master=  self, 
                                   variable = self.time_var,
                                   orient = tk.HORIZONTAL,
                                   label='Time scale',
                                   tickinterval= (self.finish_time-self.start_time)/7,
                                   from_= self.start_time,
                                   to= self.finish_time, 
                                   resolution= (self.finish_time-self.start_time)/n, 
                                   length = 250 )
            self.time_slider.grid(row=1, column=0, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W)       
            
            self.plot = MaxwellPlot(self, distribution, 'Maxwell', self.start_time)
            self.plot.grid(row=2, column=0, sticky=tk.N + tk.S + tk.E + tk.W, pady=4, padx=8)
            self.columnconfigure(0, weight=1)
            self.rowconfigure(2, weight=1)            
        else:
            label = tk.Label(master=self, text='Нет данных')
            label.grid(row=0, column=1, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)            

    def get_distribution(self, index):
        file = self.maxwell_list[index]
        print(f'{file} {index}')
        return self.race_model.read_maxwell_distribution(file)

    def update_time_var(self, var, indx, mode):
        index = int((self.n-1) * (self.time_var.get()-self.start_time) / (self.finish_time-self.start_time))
        distribution, time_stamp = self.get_distribution(index)
        self.plot.update(distribution, time_stamp)

    def update_var(self, var, indx, mode):
        distribution, time_stamp  = self.get_distribution(self.index_var.get())
        self.plot.update(distribution)

