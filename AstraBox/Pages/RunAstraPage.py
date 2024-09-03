import datetime
import tkinter as tk
import tkinter.ttk as ttk
import json
import pathlib as pathlib
import os 
from pathlib import Path
import tkinter.messagebox as messagebox

from AstraBox.Views.HeaderPanel import HeaderPanel
from AstraBox.Views.LogConsole import LogConsole
from AstraBox.Models.RunModel import RunModel
import AstraBox.Kernel as Kernel
import AstraBox.Models.AstraProfiles
from AstraBox.Widgets import StringBox
import AstraBox.Config as Config
import AstraBox.WorkSpace as WorkSpace
from AstraBox.ToolBox.ComboBox import ComboBox

import AstraBox.ToolBox.ImageButton as ImageButton

from AstraBox.Task import Task

class ConfigPanel(ttk.Frame):
    def __init__(self, master, last_task) -> None:
        super().__init__(master)        

        frame = ttk.Frame(self)
        ttk.Label(frame, text='Title:').pack(side='left')
        self.entry = ttk.Entry(frame, width= 60 )
        self.entry.pack(side='left', padx=10)
        self.entry.insert(0, last_task.title)
        frame.grid(row=0, column=0, columnspan=3, pady=4, sticky= tk.E + tk.W)  

        self.exp_combo = ComboBox(self, 'Exp:', WorkSpace.get_folder_content_list('ExpModel'))
        self.exp_combo.grid(row=1, column=0,  padx=2, sticky= tk.E + tk.W)
        self.equ_combo = ComboBox(self, 'Equ:', WorkSpace.get_folder_content_list('EquModel'))
        self.equ_combo.grid(row=1, column=1,  padx=2, sticky=tk.E + tk.W)
        fcl =  WorkSpace.get_folder_content_list('RTModel')
        if len(fcl)>0:
            self.rt_combo = ComboBox(self, 'Ray tracing:', fcl)
            self.rt_combo.grid(row=1, column=2,  padx=2, sticky= tk.E + tk.W)
        else:
            self.rt_combo= None
        self.astra_combo = ComboBox(self, 'Astra profiles:', Config.get_astra_profile_list(), width=15)
        self.astra_combo.grid(row=1, column=3,  padx=2, sticky= tk.E + tk.W)
      
        self.btn = ImageButton.create(self, '4231901.png', self.open_config)
        self.btn.grid(row=1, column=4,  padx=5, sticky= tk.E + tk.W)

        self.columnconfigure(0, weight=1)    
        self.columnconfigure(1, weight=1)    
        self.columnconfigure(2, weight=1)    

        self.exp_combo.set(last_task.exp)
        self.equ_combo.set(last_task.equ)
        if self.rt_combo:
            if last_task.rt:
                self.rt_combo.set(last_task.rt)
        self.astra_combo.set(last_task.astra_profile)      
                
    def open_config(self):
        print('open_config')
        os.system(f'start notepad {Config.get_config_path()}') 

    def get_task(self):
        print('get_task')
        task = Task(exp= self.exp_combo.get(), equ= self.equ_combo.get())
        print(task.name)
        task.title= self.entry.get()
        if self.rt_combo:
            task.rt= self.rt_combo.get()
        task.astra_profile= self.astra_combo.get()
        return task

class RunAstraPage(ttk.Frame):
    terminated = False
    def __init__(self, master) -> None:
        super().__init__(master)        
        last_task = WorkSpace.get_last_task()

        self.header_content =  { 
            "title": f"{last_task.name}", 
            "buttons":[
                ('Run', self.run),
                ('Run with Pause', self.run_with_pause),
                #('Run with timeout', self.start),
                ('Multy Run', self.multy_run),
                ('Terminate', self.terminate)
                ]
            }
        self.astra_profiles = AstraBox.Models.AstraProfiles.default()

        self.hp = HeaderPanel(self, self.header_content)
        self.hp.grid(row=0, column=0,  padx=5, sticky=tk.N + tk.S + tk.E + tk.W)
 
        self.config_panel = ConfigPanel(self, last_task)
        self.config_panel.grid(row=2, column=0, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)
        
        runframe = ttk.LabelFrame(self,  text=f"Calculation log:")
        self.log_console = LogConsole(runframe)
        self.log_console.grid(row=1, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        runframe.columnconfigure(0, weight=1)
        runframe.rowconfigure(1, weight=1)
        self.first_init = True
        #self.bind('<Visibility>', self.visibilityChanged)
        runframe.grid(row=3, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        self.rowconfigure(3, weight=1)
        self.columnconfigure(0, weight=1)        
        
    def multy_run(self):
        if messagebox.askokcancel("Run", "Do you want to Multy Run?"):
            print('run multy run')
            exp_list =  WorkSpace.get_folder_content ('ExpModel')
            equ = self.config_panel.equ_combo.get()
            for exp in exp_list:
                if self.terminated: break
                race_name = f"{self.race_name['value']}_{Path(equ).stem}-{Path(exp).stem} "
                print(race_name)
                self.single_run(race_name, exp, 'no_pause')
                #self.batch_run()

    def run_with_pause(self):
        exp = self.config_panel.exp_combo.get()
        #self.single_run(self.race_name['value'], exp, 'pause')
        task= self.config_panel.get_task()
        self.run_task(task, 'pause')

    def run(self):
        exp = self.config_panel.exp_combo.get()
        #self.single_run(self.race_name['value'], exp, 'no_pause')
        task= self.config_panel.get_task()
        self.run_task(task, 'no_pause')

    def run_task(self, task, option:str):
        self.hp.update_title(task.name)
        WorkSpace.save_last_task(task)
        self.log_console.set_logger(Kernel.get_logger())
        Kernel.set_progress_callback(self.on_progress)     
        Kernel.log_info(task)
        astra_profile = Config.get_astra_profile(task.astra_profile)
        self.on_progress(0)

        Kernel.execute(task, astra_profile, option)
        
        WorkSpace.refresh_folder('RaceModel')        

    def single_run(self, race_name, exp, option:str):
        
        equ = self.config_panel.equ_combo.get()
        rt = self.config_panel.rt_combo.get()
        astra_porfile_name = self.config_panel.astra_combo.get()
        astra_profile = Config.get_astra_profile(astra_porfile_name)
        self.save_last_run(exp, equ, rt, astra_porfile_name)

        self.log_console.set_logger(Kernel.get_logger())
        Kernel.set_progress_callback(self.on_progress)
        #Kernel.set_astra_profile(a_p)

        run_model = RunModel(name= race_name, comment= self.race_comment['value'],exp_name= exp, equ_name= equ, rt_name= rt ) 
   
        Kernel.log_info(f"exp: {exp}, equ: {equ}, rt: {rt}, astra_profile: {astra_porfile_name}")
        self.on_progress(0)

        Kernel.execute(run_model, astra_profile, option)
        
        WorkSpace.refresh_folder('RaceModel')

    def save_last_run(self, exp, equ, rt, ap):
        last_run = {'exp': exp, 'equ': equ, 'rt': rt, 'astra_profile': ap}
        WorkSpace.save_last_run(last_run)

    def terminate(self):
        self.terminated = True

    def on_progress(self, pos):
        #print('RunAstraView')
        self.master.master.update()
        self.master.master.update_idletasks()
        pass