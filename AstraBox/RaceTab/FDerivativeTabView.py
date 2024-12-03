import tkinter as tk
import tkinter.ttk as ttk
from typing import Any
import tkinter.messagebox as messagebox
import pandas as pd
from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import ( FigureCanvasTkAgg, NavigationToolbar2Tk)

from AstraBox.RaceTab.TabViewBasic import TabViewBasic
from AstraBox.Models.RaceModel import RaceModel
from AstraBox.ToolBox.MaxwellPlot import MaxwellPlot


class FDerivativeTabView(TabViewBasic):
    def __init__(self, master, model: RaceModel) -> None:
        super().__init__(master, model)  

    def init_ui(self): 
        self.maxwell_list = self.race_model.get_file_list('F_DERIVATIVE')
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
            
            self.plot = MaxwellPlot(self, distribution, 'Derivative of f', self.start_time)
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

