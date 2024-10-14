from cgitb import enable
import tkinter as tk
import tkinter.ttk as ttk
import pandas as pd
from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import ( FigureCanvasTkAgg, NavigationToolbar2Tk)

import AstraBox.Models.ModelFactory as ModelFactory

from AstraBox.Pages.InfoPanel import InfoPanel
from AstraBox.Pages.TaskPage import TaskPage
from AstraBox.Views.FRTCView import FRTCView
from AstraBox.Views.HeaderPanel import HeaderPanel
from AstraBox.Views.ExtraRaceView import ExtraRaceView


from AstraBox.Models.RaceModel import RaceModel

from AstraBox.RaceTab.RaceView import TimeSeriesView
from AstraBox.RaceTab.RaceView import RadialDataView
from AstraBox.RaceTab.RaceView import TrajectoryTab
from AstraBox.RaceTab.RaceView import RadialDrivenCurrentView
from AstraBox.RaceTab.RaceView import LHCDRadialDataView
from AstraBox.RaceTab.RaceView import MaxwellView
from AstraBox.RaceTab.RaceView import DiffusionView
from AstraBox.RaceTab.SpectrumTabView import SpectrumView
from AstraBox.RaceTab.SpectrumTabView import SpectrumTabView
from AstraBox.RaceTab.RaceView import RTResultView
from AstraBox.RaceTab.RaceView import DrivenCurrentView
from AstraBox.RaceTab.RaceView import ExecTimeView
from AstraBox.Views.SummaryView import SummaryView
from AstraBox.Views.TaskListView import TaskListView
from AstraBox.Views.TextView import TextView


class FRTCBook(ttk.Notebook):
    def __init__(self, master, model) -> None:
        super().__init__(master)        

        summary_view = SummaryView(self, model= model)
        self.add(summary_view, text="Summary", underline=0, sticky=tk.NE + tk.SW)

        if model.exp_model:
            view = TextView(self, model.exp_model, state= 'disabled')
            self.add(view, text="Exp", underline=0, sticky=tk.NE + tk.SW)   

        if model.equ_model:
            view = TextView(self, model.equ_model, state= 'disabled')
            self.add(view, text="Equ", underline=0, sticky=tk.NE + tk.SW)   

        time_series_view = TimeSeriesView(self, model= model)
        self.add(time_series_view, text="Time Series", underline=0, sticky=tk.NE + tk.SW)

        radial_data_view = RadialDataView(self, model= model)
        self.add(radial_data_view, text="Radial Data", underline=0, sticky=tk.NE + tk.SW)
        
        if model.data_files_exists('TRAJECTROY'):
            trajectory_view = TrajectoryTab(self, model= model, folder_name= 'TRAJECTROY')
            self.add(trajectory_view, text="Trajectory", underline=0, sticky=tk.NE + tk.SW)

        if model.data_files_exists('TRAJ_POS'):
            trajectory_view = TrajectoryTab(self, model= model, folder_name= 'TRAJ_POS')
            self.add(trajectory_view, text="Traj pos", underline=0, sticky=tk.NE + tk.SW)

        if model.data_files_exists('TRAJ_NEG'):
            trajectory_view = TrajectoryTab(self, model= model, folder_name= 'TRAJ_NEG')
            self.add(trajectory_view, text="Traj neg", underline=0, sticky=tk.NE + tk.SW)

        #distrib_view = DistributionView(self.notebook, model= model)
        #self.notebook.add(distrib_view, text="Distribution", underline=0, sticky=tk.NE + tk.SW)
        lhcd_radial_view = LHCDRadialDataView(self, model= model)
        self.add(lhcd_radial_view, text="LHCD Radial", underline=0, sticky=tk.NE + tk.SW)

        dc_view = RadialDrivenCurrentView(self, model= model)
        self.add(dc_view, text="Radial DC", underline=0, sticky=tk.NE + tk.SW)
        
        maxwell_view = MaxwellView(self, model= model)
        self.add(maxwell_view, text="Maxwell", underline=0, sticky=tk.NE + tk.SW)

        maxwell_view = DiffusionView(self, model= model)
        self.add(maxwell_view, text="Diffusion", underline=0, sticky=tk.NE + tk.SW)        

        if model.frtc_model:
            frtc_view = FRTCView(self, model.frtc_model, state= 'disabled')
            self.add(frtc_view, text="FRTC Param", underline=0, sticky=tk.NE + tk.SW)      

        if model.version == 'v1':
            tab_view = SpectrumView(self, model= model)
        else:
            tab_view = SpectrumTabView(self, model= model)            
        self.add(tab_view, text="Spectrum View", underline=0, sticky=tk.NE + tk.SW)      

        rt_result_view = RTResultView(self, model= model)
        self.add(rt_result_view, text="RT Result", underline=0, sticky=tk.NE + tk.SW)   

        dc_view = DrivenCurrentView(self, model= model)
        self.add(dc_view, text="Driven Current", underline=0, sticky=tk.NE + tk.SW)   

        et_view = ExecTimeView(self, model= model)
        self.add(et_view, text="Exec time", underline=0, sticky=tk.NE + tk.SW)  



class RacePage(ttk.Frame):
 
    def __init__(self, master, folder_item) -> None:
        super().__init__(master)        
        self.master = master
        self.folder_item = folder_item
        self.model = RaceModel.load(folder_item.path)  
        #self.model.load_model_data()
        title = f"Race: {self.model.name}"
        self.header_content = { "title": title, "buttons":[('Delete', self.delete_model), ('Open', self.open_new_windows), ('Extra', self.open_extra_race_view) ]}

        self.hp = HeaderPanel(self, self.header_content)
        self.hp.grid(row=0, column=0, columnspan=5, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)
        self.columnconfigure(1, weight=1)        
        self.rowconfigure(4, weight=1)    

        ip = InfoPanel(self, self.model)
        ip.grid(row=2, column=0, columnspan=5, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

        self.label = ttk.Label(self,  text='Comment:')
        self.label.grid(row=3, column=0, padx=5, pady=5)
        self.var_comment = tk.StringVar(master= self, value=self.model.read_comment())
        self.comment_entry = ttk.Entry(self, textvariable = self.var_comment)
        self.comment_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

        self.save_btn = ttk.Button(self, text='save', command=self.save_comment)
        self.save_btn.grid(row=3, column=2, padx=5, pady=5)

        match self.model.version:
            case 'v3':
                task_list_view = TaskListView(self, self.model, command= self.show_task)
                task_list_view.grid(row=4, column=0, columnspan=3, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)
            case _:
                self.notebook = FRTCBook(self, self.model)
                self.notebook.grid(row=4, column=0, columnspan=3, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)

    def show_task(self, action):
        print(action)
        new_window = tk.Toplevel(self.master)
        new_window.title("Race Window")
        new_window.geometry("1050x800")                
        model_view = TaskPage(new_window, self.folder_item, action['payload'])   
        model_view.grid(row=0, column=0, padx=10, sticky=tk.N + tk.S + tk.E + tk.W)     
        new_window.columnconfigure(0, weight=1)        
        new_window.rowconfigure(0, weight=1)    

    def save_comment(self):
        cmt = self.var_comment.get()
        self.model.write_comment(cmt)
        self.folder_item.comment = cmt
        if not self.folder_item.on_update is None:
                self.folder_item.on_update()

    def delete_model(self):
        if self.folder_item.remove():
            self.master.show_empty_view()                
        
    def open_new_windows(self):
        new_window = tk.Toplevel(self.master)
        new_window.title("Race Window")
        new_window.geometry("850x870")                
        model_view = RacePage(new_window, self.folder_item)   
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
