import datetime
import tkinter as tk
import tkinter.ttk as ttk
import json
import pathlib as pathlib
import os 
from pathlib import Path

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

class ConfigPanel(ttk.Frame):
    def __init__(self, master) -> None:
        super().__init__(master)        
        self.exp_combo = ComboBox(self, 'Exp:', ['All exp'] + WorkSpace.get_item_list('ExpModel'), width= 20)
        self.exp_combo.pack(side=tk.LEFT)
        self.equ_combo = ComboBox(self, 'Equ:', WorkSpace.get_item_list('EquModel'))
        self.equ_combo.pack(side=tk.LEFT)
        self.rt_combo = ComboBox(self, 'Ray tracing:', WorkSpace.get_item_list('RTModel'), width= 15)
        self.rt_combo.pack(side=tk.LEFT)
        self.astra_combo = ComboBox(self, 'Astra profiles:', Config.get_astra_profile_list(), width= 15)
        self.astra_combo.pack(side=tk.LEFT)
      
        btn = ImageButton.create(self, '4231901.png', self.open_config)
        btn.pack(side=tk.LEFT)

        p = WorkSpace.get_location_path('RaceModel').joinpath('last_run')
        if p.exists():
            with p.open(mode= "r") as json_file:
                last_run = json.load(json_file)
            self.exp_combo.set(last_run['exp'])
            self.equ_combo.set(last_run['equ'])
            self.rt_combo.set(last_run['rt'])
            self.astra_combo.set(last_run['astra_profile'])      
                
    def open_config(self):
        print('open_config')
        os.system(f'start notepad {Config.get_config_path()}') 

class RunAstraView(ttk.Frame):
    terminated = False
    def __init__(self, master) -> None:
        super().__init__(master)        
        self.header_content =  { "title": "Run ASTRA", "buttons":[('Run calculation', self.start), ('Terminate', self.terminate)]}
        self.astra_profiles = AstraBox.Models.AstraProfiles.default()
        self.hp = HeaderPanel(self, self.header_content)
        self.hp.grid(row=0, column=0,  padx=5, sticky=tk.N + tk.S + tk.E + tk.W)
        self.columnconfigure(0, weight=1)        
        #self.rowconfigure(0, weight=1)    

        self.race_name = {'title': 'Race name', 'value': datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}
        self.rn_wdg = StringBox(self, self.race_name, width=40)
        self.rn_wdg.grid(row=1, column=0, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)

        self.config_panel = ConfigPanel(self)
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

    def start(self):
        exp = self.config_panel.exp_combo.get()
        equ = self.config_panel.equ_combo.get()
        if exp == 'All exp':
            exp_list =  WorkSpace.get_item_list('ExpModel')
            for exp in exp_list:
                if self.terminated: break
                race_name = f"{self.race_name['value']}_{Path(equ).stem}-{Path(exp).stem} "
                print(race_name)
                self.single_run(race_name, exp)
                #self.batch_run()
        else:
            self.single_run(self.race_name['value'], exp)

    def single_run(self, race_name, exp):
        
        equ = self.config_panel.equ_combo.get()
        rt = self.config_panel.rt_combo.get()
        ap = self.config_panel.astra_combo.get()
        
        self.log_console.set_logger(Kernel.get_logger())
        Kernel.set_progress_callback(self.on_progress)
        Kernel.set_astra_profile(ap)
        run_model = RunModel(name= race_name, exp_name= exp, equ_name= equ, rt_name= rt ) 
        worker = Kernel.AstraWorker(run_model)
   
        Kernel.log_info(f"exp: {exp}, equ: {equ}, rt: {rt}, astra_profile: {ap}")
        self.on_progress(0)
        self.save_last_run(exp, equ, rt, ap)
        worker.start()
        WorkSpace.refresh('RaceModel')

    def save_last_run(self, exp, equ, rt, ap):
        last_run = {'exp': exp, 'equ': equ, 'rt': rt, 'astra_profile': ap}
        p = WorkSpace.get_location_path('RaceModel').joinpath('last_run')
        with p.open(mode= "w") as json_file:
            json.dump(last_run, json_file, indent=2)

    def terminate(self):
        self.terminated = True

    def on_progress(self, pos):
        #print('RunAstraView')
        self.master.master.update()
        self.master.master.update_idletasks()
        pass