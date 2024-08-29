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

class ConfigPanel(ttk.Frame):
    def __init__(self, master) -> None:
        super().__init__(master)        
        self.exp_combo = ComboBox(self, 'Exp:', WorkSpace.get_folder_content('ExpModel'))
        self.exp_combo.grid(row=0, column=0,  padx=2, sticky= tk.E + tk.W)
        self.equ_combo = ComboBox(self, 'Equ:', WorkSpace.get_folder_content('EquModel'))
        self.equ_combo.grid(row=0, column=1,  padx=2, sticky=tk.E + tk.W)
        self.rt_combo = ComboBox(self, 'Ray tracing:', WorkSpace.get_folder_content('RTModel'))
        self.rt_combo.grid(row=0, column=2,  padx=2, sticky= tk.E + tk.W)
        self.astra_combo = ComboBox(self, 'Astra profiles:', Config.get_astra_profile_list(), width=15)
        self.astra_combo.grid(row=0, column=3,  padx=2, sticky= tk.E + tk.W)
      
        self.btn = ImageButton.create(self, '4231901.png', self.open_config)
        self.btn.grid(row=0, column=4,  padx=5, sticky= tk.E + tk.W)

        self.columnconfigure(0, weight=1)    
        self.columnconfigure(1, weight=1)    
        self.columnconfigure(2, weight=1)    
        #self.columnconfigure(3, weight=1)    
  

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

class RunAstraPage(ttk.Frame):
    terminated = False
    def __init__(self, master) -> None:
        super().__init__(master)        
        self.race_name = {
            'title': 'Race name',
             'value': datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            }

        self.header_content =  { 
            "title": f"{self.race_name['value']}", 
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
 
        self.race_name = {'title': 'Race name', 'value': datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}
        self.race_comment = {'title': 'Comment', 'value': 'enter comment'}
        self.rn_wdg = StringBox(self, self.race_comment, width=40)
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
        self.single_run(self.race_name['value'], exp, 'pause')

    def run(self):
        exp = self.config_panel.exp_combo.get()
        self.single_run(self.race_name['value'], exp, 'no_pause')

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