from cgitb import enable
import tkinter as tk
import tkinter.ttk as ttk
import pandas as pd
from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import ( FigureCanvasTkAgg, NavigationToolbar2Tk)

import AstraBox.Models.ModelFactory as ModelFactory

from AstraBox.Views.HeaderPanel import HeaderPanel
from AstraBox.Views.ExtraRaceView import ExtraRaceView


from AstraBox.Models.RaceModel import RaceModel

from AstraBox.Views.RaceView import TimeSeriesView
from AstraBox.Views.RaceView import RadialDataView
from AstraBox.Views.RaceView import TrajectoryTab
from AstraBox.Views.RaceView import RadialDrivenCurrentView
from AstraBox.Views.RaceView import MaxwellView
from AstraBox.Views.RaceView import DiffusionView
from AstraBox.Views.RaceView import SpectrumView
from AstraBox.Views.RaceView import RTResultView
from AstraBox.Views.RaceView import DrivenCurrentView
from AstraBox.Views.RaceView import ExecTimeView
from AstraBox.Views.SummaryView import SummaryView

class InfoPanel(tk.Frame):
    def __init__(self, master, model) -> None:
        super().__init__(master) #, text= 'Race info')
        info = {
            'Exp:': model.data['ExpModel']['name'],
            'Equ:': model.data['EquModel']['name'],
            
            }
        if 'RTModel' in  model.data:
            info['Ray tracing:'] = model.data['RTModel']['name']
        for key, value in info.items():
            var = tk.StringVar(master= self, value=value)
            label = tk.Label(master=self, text=key)
            label.pack(side = tk.LEFT, ipadx=10)		
            entry = tk.Entry(self, width=20, textvariable= var, state='disabled')
            entry.pack(side = tk.LEFT)

class RacePage(ttk.Frame):
 
    def __init__(self, master, model: RaceModel) -> None:
        super().__init__(master)        
        self.master = master
        self.model = model
        self.model.load_model_data()
        title = f"Race: {self.model.name}"
        self.header_content = { "title": title, "buttons":[('Delete', self.delete_model), ('New windows', self.open_new_windows), ('Extra', self.open_extra_race_view) ]}

        self.hp = HeaderPanel(self, self.header_content)
        self.hp.grid(row=0, column=0, columnspan=5, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)
        self.columnconfigure(0, weight=1)        
        self.rowconfigure(3, weight=1)    

        ip = InfoPanel(self, model)
        ip.grid(row=2, column=0, columnspan=5, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=3, column=0, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)

        summary_view = SummaryView(self.notebook, model= model)
        self.notebook.add(summary_view, text="Summary", underline=0, sticky=tk.NE + tk.SW)


        time_series_view = TimeSeriesView(self.notebook, model= model)
        self.notebook.add(time_series_view, text="Time Series", underline=0, sticky=tk.NE + tk.SW)

        radial_data_view = RadialDataView(self.notebook, model= model)
        self.notebook.add(radial_data_view, text="Radial Data", underline=0, sticky=tk.NE + tk.SW)
        
        if model.data_files_exists('TRAJECTROY'):
            trajectory_view = TrajectoryTab(self.notebook, model= model, folder_name= 'TRAJECTROY')
            self.notebook.add(trajectory_view, text="Trajectory", underline=0, sticky=tk.NE + tk.SW)

        if model.data_files_exists('TRAJ_POS'):
            trajectory_view = TrajectoryTab(self.notebook, model= model, folder_name= 'TRAJ_POS')
            self.notebook.add(trajectory_view, text="Traj pos", underline=0, sticky=tk.NE + tk.SW)

        if model.data_files_exists('TRAJ_NEG'):
            trajectory_view = TrajectoryTab(self.notebook, model= model, folder_name= 'TRAJ_NEG')
            self.notebook.add(trajectory_view, text="Traj neg", underline=0, sticky=tk.NE + tk.SW)

        #distrib_view = DistributionView(self.notebook, model= model)
        #self.notebook.add(distrib_view, text="Distribution", underline=0, sticky=tk.NE + tk.SW)
        dc_view = RadialDrivenCurrentView(self.notebook, model= model)
        self.notebook.add(dc_view, text="Radial DC", underline=0, sticky=tk.NE + tk.SW)
        
        maxwell_view = MaxwellView(self.notebook, model= model)
        self.notebook.add(maxwell_view, text="Maxwell", underline=0, sticky=tk.NE + tk.SW)

        maxwell_view = DiffusionView(self.notebook, model= model)
        self.notebook.add(maxwell_view, text="Diffusion", underline=0, sticky=tk.NE + tk.SW)        

        spectrum_view = SpectrumView(self.notebook, model= model)
        self.notebook.add(spectrum_view, text="Spectrum View", underline=0, sticky=tk.NE + tk.SW)      

        rt_result_view = RTResultView(self.notebook, model= model)
        self.notebook.add(rt_result_view, text="RT Result", underline=0, sticky=tk.NE + tk.SW)   

        dc_view = DrivenCurrentView(self.notebook, model= model)
        self.notebook.add(dc_view, text="Driven Current", underline=0, sticky=tk.NE + tk.SW)   

        et_view = ExecTimeView(self.notebook, model= model)
        self.notebook.add(et_view, text="Exec time", underline=0, sticky=tk.NE + tk.SW)  

    def delete_model(self):
        if self.model:
            if ModelFactory.delete_model(self.model):
                self.master.show_empty_view()
        
    def open_new_windows(self):
        new_window = tk.Toplevel(self.master)
        new_window.title("Race Window")
        new_window.geometry("850x870")                
        model_view = RacePage(new_window, self.model)   
        model_view.grid(row=0, column=0, padx=10, sticky=tk.N + tk.S + tk.E + tk.W)     
        new_window.columnconfigure(0, weight=1)        
        new_window.rowconfigure(0, weight=1)    

    def open_extra_race_view(self):
        new_window = tk.Toplevel(self.master)
        new_window.title("Extra Race View")
        new_window.geometry("1150x700")                
        model_view = ExtraRaceView(new_window, self.model)   
        model_view.grid(row=0, column=0, padx=10, sticky=tk.N + tk.S + tk.E + tk.W)   

    def destroy(self):
        print("RaceView destroy")
        super().destroy()   
