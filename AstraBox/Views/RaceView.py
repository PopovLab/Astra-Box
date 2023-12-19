from cgitb import enable
import tkinter as tk
import tkinter.ttk as ttk
from typing import Any
from typing_extensions import Literal
import pandas as pd
from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import ( FigureCanvasTkAgg, NavigationToolbar2Tk)

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
from AstraBox.ToolBox.MaxwellPlot import MaxwellPlot
from AstraBox.ToolBox.ExecTimePlot import ExecTimePlot

class InfoPanel(tk.Frame):
    def __init__(self, master, model) -> None:
        super().__init__(master) #, text= 'Race info')
        info = {
            'Exp:': model.data['ExpModel']['name'],
            'Equ:': model.data['EquModel']['name'],
            
            }
        if 'RTModel' in  model.data.keys():
            info['Ray tracing:'] : model.data['RTModel']['name']
        for key, value in info.items():
            var = tk.StringVar(master= self, value=value)
            label = tk.Label(master=self, text=key)
            label.pack(side = tk.LEFT, ipadx=10)		
            entry = tk.Entry(self, width=15, textvariable= var, state='disabled')
            entry.pack(side = tk.LEFT)


class TabViewBasic(ttk.Frame):
    """Базовый класс для вкладок, для перехвата события видимости, что бы потом инициализировать вкладку"""

    def __init__(self, master, model: RaceModel) -> None:
        super().__init__(master)  
        self.race_model = model

        self.first_time = True
        self.bind('<Visibility>', self.visibilityChanged)
    
    def visibilityChanged(self, event):
        if self.first_time:
            self.first_time = False
            self.init_ui()

    def init_ui(self):
        print('init TabViewBasic')
        pass

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
        self.rowconfigure(2, weight=1)


from AstraBox.ToolBox.SpectrumPlot import SpectrumChart, ScatterPlot2D3D
from AstraBox.Views.SheetView import SheetView

class SpectrumView(TabViewBasic):
    def __init__(self, master, model: RaceModel) -> None:
        super().__init__(master, model)  

    def init_ui(self):
        print('create SpectrumView')
        self.spectrum_model = self.race_model.get_spectrum()
        self.rt = self.race_model.data['RTModel']['setting']
        #print(self.spectrum_model.get_dest_path())
        self.spectrums = {}
        self.spectrums['origin'] = self.spectrum_model.spectrum_data
        #self.spectrums['origin2'] = self.read_spectrum('spectrum.dat')
        self.spectrums['full_spectrum'] = self.read_spectrum('full_spectrum.dat')        
        self.spectrums['spectrum_pos'] = self.read_spectrum('spectrum_pos.dat')
        self.spectrums['spectrum_neg'] = self.read_spectrum('spectrum_neg.dat')        
        self.spectrums['nteta'] = self.rt['grill parameters']['ntet']['value']

        summary = self.make_summary()
        summary.grid(row=0, column=0, padx=15, pady=15, sticky=tk.N + tk.S + tk.E + tk.W)
        plot = self.make_spectrum_plot()
        plot.grid(row=1, column=0, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
    
    def read_spectrum(self, fname):
        spectr = self.race_model.read_dat_no_header(f'lhcd/{fname}')
        if spectr is not None:
            spectr=  spectr.set_axis(['Ntor', 'Npol', 'Amp'], axis=1)
            if spectr['Ntor'][0] > spectr['Ntor'].iat[-1]:
                spectr = spectr.iloc[::-1]
                
            return spectr
        else:
            return None
        
    def item_str(self, k1, k2):
        #print(self.rt)
        item = self.rt[k1][k2]
        return f"{item['title']}:  {item['value']}"

    def make_summary(self):
        #summ = tk.Label(master=self, text='Место для RT model')
        values = []
        values.append(self.item_str('Physical parameters', 'Freq'))
        values.append(self.item_str('Numerical parameters', 'nr'))
        values.append(self.item_str('Numerical parameters', 'eps'))
        values.append(self.item_str('Options', 'inew'))
        values.append(self.item_str('grill parameters', 'Zplus'))
        values.append(self.item_str('grill parameters', 'Zminus'))
        values.append(self.item_str('grill parameters', 'ntet'))
        values.append(self.item_str('grill parameters', 'nnz'))
        
        summ = SheetView(self, values)
        return summ
    
    def make_spectrum_plot(self):
        if type(self.spectrum_model.spectrum_data) is dict:
            print('загрузил спектр')
            print(len(self.spectrum_model.spectrum_data['Ntor']))
            match self.spectrum_model.spectrum_type:
                case 'gaussian'|'spectrum_1D':
                    #plot = SpectrumPlot(self, self.spectrum_model.spectrum_data['Ntor'], self.spectrum_model.spectrum_data['Amp']  )
                    #plot = SpectrumPlot(self, spectrum_list= self.all_spectrum)
                    plot = SpectrumChart(self, self.spectrums)
                case 'scatter_spectrum':
                    plot = ScatterPlot2D3D(self, self.spectrum_model.spectrum_data)
                case 'spectrum_2D':
                    pass       
        else:
            print(self.spectrum_model.spectrum_data)
            plot = tk.Label(master=self, text='Нет данных')
        
        return plot
    

from AstraBox.Models.TrajectoryModel import TrajectoryModel
from AstraBox.Models.TrajectoryModel import path_to_time
from AstraBox.ToolBox.TrajectoryPlot_v2 import TrajectoryPlot_v2

from AstraBox.Views.tkSliderWidget import Slider


def print_traj_series(ts, time):
    print(f"len = {len(ts)} time={time}")
    print(f"Theta= {ts[0]['theta']}, index = {ts[0]['index']}, mbad= {ts[0]['mbad']}")

class TrajectoryView_v2(tk.Frame):
    def __init__(self, master, traj_model: TrajectoryModel) ->None:
        super().__init__(master)  
        self.traj_model = traj_model
        self.traj_model.select_series(0)

        plasma_bound = self.traj_model.race_model.read_plasma_bound()

        self.plot = TrajectoryPlot_v2(self, self.traj_model, plasma_bound)
        self.plot.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W, pady=4, padx=8)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)


    

    def select_moment(self, index):
        print(index)
        self.time_stamp = path_to_time(self.traj_model.trajectory_series_list[index])
        self.traj_model.select_series(index)
        #traj_series['time'] = time_stamp
        print_traj_series(self.traj_model.traj_series, self.time_stamp)
        
        #self.update_view()

class TrajectoryView_v1(tk.Frame):
    def __init__(self, master, traj_model: TrajectoryModel) ->None:
        super().__init__(master)  
        self.traj_model = traj_model
        self.rays = traj_model.rays
        self.time_stamp = traj_model.start_time
        plasma_bound = self.traj_model.race_model.read_plasma_bound()
        self.index_1 = tk.IntVar(master = self, value=0)
        self.index_1.trace_add('write', self.update_plot)
        self.slider_1 = tk.Scale(master=  self, variable = self.index_1, orient = tk.HORIZONTAL, 
                                sliderlength = 20,
                                width = 10,            
                                label='start ray',
                                tickinterval= len(self.rays)/4,
                                from_=0, 
                                to=len(self.rays)-1, 
                                resolution=1 )
        self.slider_1.grid(row=1, column=0, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W) 

        self.index_2 = tk.IntVar(master = self, value= len(self.rays)-1 if len(self.rays)<500 else 500)
        self.index_2.trace_add('write', self.update_plot)
        self.slider_2 = tk.Scale(master=  self, variable = self.index_2, orient = tk.HORIZONTAL,
                                sliderlength = 20,
                                width = 10,            
                                label='numbers of ray',
                                tickinterval= len(self.rays)/4,
                                from_=0, 
                                to=len(self.rays)-1, 
                                resolution=1 )
        self.slider_2.grid(row=1, column=1, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W) 

        self.plot = TrajectoryPlot(self, self.rays, self.time_stamp, plasma_bound)
        self.plot.grid(row=2, column=0, columnspan=2, sticky=tk.N + tk.S + tk.E + tk.W, pady=4, padx=8)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        
        self.len_rays = len(self.rays)

    def update_plot(self, var, indx, mode):
        self.update_view()

    def update_view(self):
        i1 = self.index_1.get()
        i2 = i1 + self.index_2.get()
        if self.len_rays != len(self.rays):
            self.len_rays = len(self.rays)
            print(f'update sliders {self.len_rays}')
            self.slider_1.configure(tickinterval= self.len_rays/4, to=self.len_rays-1)
            self.slider_2.configure(tickinterval= self.len_rays/4, to=self.len_rays-1)
        if i2>self.len_rays: i2 = self.len_rays
        if i1>self.len_rays: i1 = self.len_rays
        self.plot.update(self.rays[i1:i2], self.time_stamp)

    def select_moment(self, index):
        self.rays, self.time_stamp = self.traj_model.get_rays(index)
        self.update_view()

class TrajectoryTab(TabViewBasic):
    def __init__(self, master, model: RaceModel, folder_name: str) -> None:
        super().__init__(master, model)  
        self.folder_name = folder_name
        self.race_model = model

    def init_ui(self): 

        self.traj_model = TrajectoryModel(self.race_model, self.folder_name)
        if self.traj_model.num_traj>0: 

            self.start_time  = self.traj_model.start_time
            self.finish_time  = self.traj_model.finish_time

            n = self.traj_model.num_traj

            self.time_var = tk.DoubleVar(master = self, value=self.start_time)
            self.time_var.trace_add('write', self.update_plot)

            self.time_slider = tk.Scale(master=  self, 
                                   variable = self.time_var,
                                   orient = tk.HORIZONTAL,
                                   sliderlength = 20,
                                   width = 10,
                                   label='Time scale',
                                   tickinterval= (self.finish_time-self.start_time)/7,
                                   from_= self.start_time,
                                   to= self.finish_time, 
                                   resolution= (self.finish_time-self.start_time)/n )
            self.time_slider.grid(row=0, column=0, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W)   

            match self.traj_model.version:
                case 2: self.traj_view = TrajectoryView_v2(self, self.traj_model)
                case 1: self.traj_view = TrajectoryView_v1(self, self.traj_model)

            self.traj_view.grid(row=1, column=0, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W)   

            self.columnconfigure(0, weight=1)
            self.rowconfigure(1, weight=1)

        else:
            label = tk.Label(master=self, text='Нет данных')
            label.grid(row=0, column=1, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)            

    def update_plot(self, var, indx, mode):
        index = int((self.traj_model.num_traj-1) * (self.time_var.get()-self.start_time) / (self.finish_time-self.start_time))
        self.traj_view.select_moment(index)



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



class DiffusionView(TabViewBasic):
    def __init__(self, master, model: RaceModel) -> None:
        super().__init__(master, model)  

    def init_ui(self): 
        self.file_list = self.race_model.get_file_list('DIFFUSION')
        n = len(self.file_list)
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
            
            self.plot = SeriesPlot(self, distribution, 'Diffusion', self.start_time, уscale_log=False)
            self.plot.grid(row=2, column=0, sticky=tk.N + tk.S + tk.E + tk.W, pady=4, padx=8)
            self.columnconfigure(0, weight=1)
            self.rowconfigure(2, weight=1)
        else:
            label = tk.Label(master=self, text='Нет данных')
            label.grid(row=0, column=1, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)            

    def get_distribution(self, index):
        file = self.file_list[index]
        print(f'{file} {index}')
        return self.race_model.read_diffusion(file)

    def update_time_var(self, var, indx, mode):
        index = int((self.n-1) * (self.time_var.get()-self.start_time) / (self.finish_time-self.start_time))
        distribution, time_stamp = self.get_distribution(index)
        self.plot.update(distribution, time_stamp)

    def update_var(self, var, indx, mode):
        distribution, time_stamp  = self.get_distribution(self.index_var.get())
        self.plot.update(distribution)        