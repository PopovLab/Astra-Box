import tkinter as tk
import tkinter.ttk as ttk
from typing import Any
import tkinter.messagebox as messagebox
import pandas as pd
from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import ( FigureCanvasTkAgg, NavigationToolbar2Tk)
from AstraBox.ToolBox.VerticalNavigationToolbar import VerticalNavigationToolbar2Tk

from AstraBox.RaceTab.TabViewBasic import TabViewBasic
from AstraBox.Models.RaceModel import RaceModel
from AstraBox.ToolBox.MaxwellPlot import MaxwellPlot

class PoloidalPlot(ttk.Frame):

    def __init__(self, master, plasma_bound, equilibrium) -> None:
        super().__init__(master)  
        self.plasma_bound = plasma_bound
        self.fig = plt.figure(figsize=(6,6))
        self.axis = self.fig.subplots(1, 1)
        self.fig.suptitle(f"Poloidal view. time={equilibrium['time_stamp']}")
        self.axis.plot(self.plasma_bound['R'], self.plasma_bound['Z'])
        self.init_axis()
        self.draw_all()
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.draw()

        self.canvas.get_tk_widget().grid(row=2, column=1,columnspan=2, rowspan= 3, sticky=tk.N + tk.S + tk.E + tk.W)
        #toobar = NavigationToolbar2Tk(self.canvas, self, pack_toolbar=False)
        #toobar.grid(row=0, column=0, sticky=tk.W)
        tb = VerticalNavigationToolbar2Tk(self.canvas, self)
        tb.update()
        tb.grid(row=2, column=0, sticky=tk.N)    
        lbl = tk.Label(master=self, text='v2')
        lbl.grid(row=3, column=0, sticky=tk.N) 
        #btn = ImageButton.create(self, 'gear.png', self.show_option_windows)
        #btn.grid(row=4, column=0, sticky=tk.N) 
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(2, weight=1)

    def init_axis(self):
        pass
             
    def draw_all(self, save_lim= False):
        pass    

class PoloidalView(tk.Frame):
    def __init__(self, master, race_model: RaceModel, equilibrium: dict) ->None:
        super().__init__(master)  
        self.race_model = race_model
        self.equilibrium = equilibrium

        plasma_bound = self.race_model.read_plasma_bound()

        self.plot = PoloidalPlot(self, plasma_bound, equilibrium)
        self.plot.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W, pady=4, padx=8)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)    


class EquilibriumTabView(TabViewBasic):
    def __init__(self, master, model: RaceModel) -> None:
        super().__init__(master, model)  


    def init_ui(self): 
        self.equilibrium_list = self.race_model.get_file_list('EQUILIBRIUM')
        n = len(self.equilibrium_list)
        if n>0: 
            self.start_time  =  self.get_time_stamp(0)
            self.finish_time  = self.get_time_stamp(n-1)
            self.n = n
            equilibrium = self.get_equilibrium(0)
            print(equilibrium['GEOMETRY'])
            equilibrium['time_stamp'] = self.start_time
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
            
            self.plot = PoloidalView(self, self.race_model, equilibrium)
            self.plot.grid(row=2, column=0, sticky=tk.N + tk.S + tk.E + tk.W, pady=4, padx=8)
            self.columnconfigure(0, weight=1)
            self.rowconfigure(2, weight=1)            
        else:
            label = tk.Label(master=self, text='Нет данных')
            label.grid(row=0, column=1, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)            

    def get_equilibrium(self, index) -> dict:
        file = self.equilibrium_list[index]
        print(f'{file} {index}')
        return self.race_model.read_equilibrium(file)
    
    def get_time_stamp(self, index) -> float | None:
        file = self.equilibrium_list[index]
        print(f'{file} {index}')
        return self.race_model.get_time_stamp(file)


    def update_time_var(self, var, indx, mode):
        index = int((self.n-1) * (self.time_var.get()-self.start_time) / (self.finish_time-self.start_time))
        time_stamp = self.get_time_stamp(index)
        equilibrium = self.get_equilibrium(index)
        print(equilibrium['GEOMETRY'])
        #self.plot.update(distribution, time_stamp)
