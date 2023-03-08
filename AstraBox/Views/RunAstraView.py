import datetime
import tkinter as tk
import tkinter.ttk as ttk
import json

from AstraBox.Views.HeaderPanel import HeaderPanel
from AstraBox.Views.LogConsole import LogConsole
from AstraBox.Models.RunModel import RunModel
import AstraBox.Kernel as Kernel
import AstraBox.Models.AstraProfiles
from AstraBox.Widgets import StringBox
import AstraBox.Config as Config
import AstraBox.WorkSpace as WorkSpace
from AstraBox.ToolBox.ComboBox import ComboBox

class RunAstraView(ttk.Frame):
    def __init__(self, master) -> None:
        super().__init__(master)        
        self.header_content =  { "title": "Run ASTRA", "buttons":[('Run calculation', self.start), ('Terminate', self.terminate)]}
        self.astra_profiles = AstraBox.Models.AstraProfiles.default()
        self.hp = HeaderPanel(self, self.header_content)
        self.hp.grid(row=0, column=0, columnspan=5, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)
        self.columnconfigure(4, weight=1)        
        #self.rowconfigure(0, weight=1)    

        self.race_name = {'title': 'Race name', 'value': datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}
        self.rn_wdg = StringBox(self, self.race_name, width=30)
        self.rn_wdg.grid(row=1, column=0, columnspan=2, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)

        self.exp_combo = ComboBox(self, 'Exp', WorkSpace.getDataSource('exp').get_keys_list())
        self.exp_combo.grid(row=2, column=0, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)
        self.equ_combo = ComboBox(self, 'Equ', WorkSpace.getDataSource('equ').get_keys_list())
        self.equ_combo.grid(row=2, column=1, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)        
        self.rt_combo = ComboBox(self, 'Ray tracing', WorkSpace.getDataSource('ray_tracing').get_keys_list())
        self.rt_combo.grid(row=2, column=2, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)
        self.astra_combo = ComboBox(self, 'Astra profiles', Config.get_astra_profile_list())
        self.astra_combo.grid(row=2, column=3, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)

        self.restore_last_run()

        runframe = ttk.LabelFrame(self,  text=f"Calculation log:")
        self.log_console = LogConsole(runframe)
        self.log_console.grid(row=1, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        runframe.columnconfigure(0, weight=1)
        runframe.rowconfigure(1, weight=1)
        self.first_init = True
        #self.bind('<Visibility>', self.visibilityChanged)
        runframe.grid(row=3, column=0, columnspan=5,  sticky=tk.N + tk.S + tk.E + tk.W)
        self.rowconfigure(3, weight=1)

    def restore_last_run(self):
        ds = WorkSpace.getDataSource('races')
        p = ds.destpath.joinpath('last_run')
        if p.exists():
            with p.open(mode= "r") as json_file:
                last_run = json.load(json_file)
            self.exp_combo.set(last_run['exp'])
            self.equ_combo.set(last_run['equ'])
            self.rt_combo.set(last_run['rt'])
            self.astra_combo.set(last_run['astra_profile'])          

    def start(self):
        exp = self.exp_combo.get()
        equ = self.equ_combo.get()
        rt = self.rt_combo.get()
        ap = self.astra_combo.get()
        
        race_model = RunModel(name= self.race_name['value'], exp_name= exp, equ_name= equ, rt_name= rt ) 
        
        astra_profile = Config.get_astra_profile(ap)
        self.worker = Kernel.AstraWorker(race_model, astra_profile)
        self.log_console.set_logger(self.worker.logger)
        self.worker.on_progress = self.on_progress
        self.on_progress(0)
        ds = WorkSpace.getDataSource('races')
        last_run = {'exp': exp, 'equ': equ, 'rt': rt, 'astra_profile': ap}
        p = ds.destpath.joinpath('last_run')
        with p.open(mode= "w") as json_file:
            json.dump(last_run, json_file, indent=2)

        self.worker.start()

        ds.refresh()

    def terminate(self):
        pass

    def on_progress(self, pos):
        print('RunAstraView')
        self.master.update()
        pass