
import tkinter as tk
import tkinter.ttk as ttk

import numpy as np
import pandas as pd

from AstraBox.Models.RaceModel import RaceModel
from AstraBox.RaceTab.TabViewBasic import TabViewBasic
from AstraBox.RaceTab.LHCDRadialPlot import LHCDRadialPlot
from AstraBox.ToolBox.SpectrumPlot import SpectrumChart, ScatterPlot2D3D
from AstraBox.Views.SheetView import SheetView
from AstraBox.Views.SpectrumView import OptionsPanel

import pathlib

def create_time_index(source):
    res = []
    for fn in source:
        p = pathlib.Path(fn)
        if p.suffix == '.dat': 
            time_stamp = float(p.stem)
        else:
            time_stamp = -1
        #print(time_stamp) 
        res.append(time_stamp)
    return res

class LHCDRadialDataView(TabViewBasic):
    def __init__(self, master, model: RaceModel) -> None:
        super().__init__(master, model)  

    def make_time_index(self):
        self.time_index = []
        if len(self.pos_list)>len(self.neg_list):
            self.time_index = create_time_index(self.pos_list)
        else:
            self.time_index = create_time_index(self.neg_list)
       # print(self.time_index)
        

    def find_time_index(self, time):
        for i, tm in enumerate(self.time_index):
            if tm>time:
                return i
        return 0


    def init_ui(self):   
        self.pos_list = self.race_model.get_file_list('POWER_POS')
        self.neg_list = self.race_model.get_file_list('POWER_NEG')
        self.dc_list = self.race_model.get_file_list('DC')
        #n = min(len(self.pos_list),len(self.neg_list))
        n = len(self.dc_list)
        print(f'n= {n}')
        if n>0: 
            self.make_time_index()
            lhcd_data = self.get_lhcd_data(0)
            self.start_time = lhcd_data['cur']["Time"]
            self.finish_time = self.get_lhcd_data(n-1)['cur']["Time"]
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
            
            self.plot = LHCDRadialPlot(self, lhcd_data)
            self.plot.grid(row=2, column=0, sticky=tk.N + tk.S + tk.E + tk.W, pady=4, padx=8)
            self.columnconfigure(0, weight=1)
            self.rowconfigure(2, weight=1)
        else:
            label = tk.Label(master=self, text='Нет данных')
            label.grid(row=0, column=1, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)

    def get_lhcd_data(self, index):
        lhcd_data = {}

        file = self.dc_list[index]
        print(f'{file} {index}')
        lhcd_data['cur'] = self.race_model.read_dc_data(file)
        time_index = self.find_time_index(lhcd_data['cur']['Time'])
        #print(time_index)
        if time_index<0: return lhcd_data
        if len(self.pos_list)>time_index:
            file = self.pos_list[time_index]
            #print(f'{file} {time_index}')
            lhcd_data['pos'] = self.race_model.read_dc_data(file)
        else:
            lhcd_data['pos'] = None

        if len(self.neg_list)>time_index:
            file = self.neg_list[time_index]
            #rint(f'{file} {time_index}')
            lhcd_data['neg'] = self.race_model.read_dc_data(file)
        else:
            lhcd_data['neg'] = None
        


        return lhcd_data
    
    def update_time_var(self, var, indx, mode):
        index = int((self.n-1) * (self.time_var.get()-self.start_time) / (self.finish_time-self.start_time))
        lhcd_data = self.get_lhcd_data(index)
        self.plot.update(lhcd_data)