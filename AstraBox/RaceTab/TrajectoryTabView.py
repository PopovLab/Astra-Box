#from cgitb import enable
import tkinter as tk
import tkinter.ttk as ttk
from typing import Any
import tkinter.messagebox as messagebox
import pandas as pd
from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import ( FigureCanvasTkAgg, NavigationToolbar2Tk)

from AstraBox import WorkSpace
from AstraBox.Models.RaceModel import RaceModel
from AstraBox.Models.TrajectoryModel import TrajectoryModel
from AstraBox.Models.TrajectoryModel import path_to_time
from AstraBox.RaceTab.TabViewBasic import TabViewBasic
from AstraBox.ToolBox.TrajectoryPlot import TrajectoryPlot
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

    def save_figure(self, file_name):
        self.plot.save_figure(file_name)

    def select_moment(self, index):
        print(index)
        self.time_stamp = path_to_time(self.traj_model.trajectory_series_list[index])
        self.traj_model.select_series(index)
        self.plot.update()
        #traj_series['time'] = time_stamp
        #print_traj_series(self.traj_model.traj_series, self.time_stamp)
        
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
        self.index = 0 
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

            bnt_prev= ttk.Button(self, text='<', width=2, command= self.prev)
            bnt_prev.grid(row=0, column=1, padx=2, pady=5) 
            bnt_next= ttk.Button(self,text='>', width=2, command= self.next)
            bnt_next.grid(row=0, column=2,  padx=2, pady=5) 

            bnt= ttk.Button(self, text='!',width=2, command= self.make_magic)
            bnt.grid(row=0, column=3, padx=5, pady=5) 

            match self.traj_model.version:
                case 2: self.traj_view = TrajectoryView_v2(self, self.traj_model)
                case 1: self.traj_view = TrajectoryView_v1(self, self.traj_model)

            self.traj_view.grid(row=1, column=0, columnspan=4, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W)   

            self.columnconfigure(0, weight=1)
            self.rowconfigure(1, weight=1)

        else:
            label = tk.Label(master=self, text='Нет данных')
            label.grid(row=0, column=1, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)            

    def update_plot(self, var, indx, mode):
        idx = (self.traj_model.num_traj-1) * (self.time_var.get()-self.start_time) / (self.finish_time-self.start_time)
        index = int(idx + 0.1)
        #print(f"update {index} {idx}")
        if self.index != index:
            self.index = index
            self.traj_view.select_moment(index)

    def make_magic(self):
        '''create albom of poloidal views'''
        if messagebox.askokcancel("Make Magick", "Are you sure?"):
            print('Make Magick')
            tmp= WorkSpace.temp_folder_location().joinpath(self.traj_model.race_model.stem)
            if not tmp.exists():
                print(f"make dir {tmp}")
                tmp.mkdir()
            for index in range(self.traj_model.num_traj):
                print(f'index= {index}')
                self.traj_view.select_moment(index)
                p= tmp.joinpath(f'{index:04}.png')
                print(p.as_posix())
                self.traj_view.save_figure(p.as_posix())
            print('magick finita')

    def next(self):
        if self.index < self.traj_model.num_traj-1:
            self.index = self.index + 1
            #print(f"next {self.index}")
            self.traj_view.select_moment(self.index)
            t = self.start_time + self.index*(self.finish_time-self.start_time)/(self.traj_model.num_traj-1)
            #print(f"t {t}")
            self.time_var.set(t)

    def prev(self):
        if self.index >0:
            self.index = self.index - 1
            self.traj_view.select_moment(self.index)
            t = self.start_time + self.index*(self.finish_time-self.start_time)/(self.traj_model.num_traj-1)
            self.time_var.set(t)
