
import tkinter as tk
import tkinter.ttk as ttk

import numpy as np
import pandas as pd

from AstraBox.Models.RaceModel import RaceModel
from AstraBox.RaceTab.TabViewBasic import TabViewBasic
from AstraBox.ToolBox.LHCDRadialPlot import LHCDRadialPlot
from AstraBox.ToolBox.SpectrumPlot import SpectrumChart, ScatterPlot2D3D
from AstraBox.Views.SheetView import SheetView
from AstraBox.Views.SpectrumView import OptionsPanel

class LHCDRadialDataView(TabViewBasic):
    def __init__(self, master, model: RaceModel) -> None:
        super().__init__(master, model)  

    def init_ui(self):   
        self.pos_list = self.race_model.get_file_list('POWER_POS')
        self.neg_list = self.race_model.get_file_list('POWER_NEG')
        n = min(len(self.pos_list),len(self.neg_list))
        print(f'n= {n}')
        if n>0: 
            lhcd_data = self.get_lhcd_data(0)
            self.start_time = lhcd_data['pos']["Time"]
            self.finish_time = self.get_lhcd_data(n-1)['pos']["Time"]
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
        file = self.pos_list[index]
        print(f'{file} {index}')
        lhcd_data['pos'] = self.race_model.read_dc_data(file)

        file = self.neg_list[index]
        print(f'{file} {index}')
        lhcd_data['neg'] = self.race_model.read_dc_data(file)
        return lhcd_data
    
    def update_time_var(self, var, indx, mode):
        index = int((self.n-1) * (self.time_var.get()-self.start_time) / (self.finish_time-self.start_time))
        lhcd_data = self.get_lhcd_data(index)
        self.plot.update(lhcd_data)