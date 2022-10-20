import datetime
import tkinter as tk
import tkinter.ttk as ttk
from AstraBox.Views.HeaderPanel import HeaderPanel
from AstraBox.Storage import Storage
from AstraBox.Views.LogConsole import LogConsole
from AstraBox.Models.RaceModel import RaceModel
import AstraBox.Kernel as Kernel
import AstraBox.Models.AstraProfiles
from AstraBox.Widgets import StringBox
import AstraBox.Config as Config

class ComboBox(ttk.Frame):
    def combo_selected(self, *args):
        self.selected_value = self.combo.get()
        
    def __init__(self, master, title, values) -> None:
        super().__init__(master)     
        self.selected_value = None
        label = ttk.Label(self, text=title, width=20)
        label.grid(row=0, column=0, sticky=tk.W, pady=4, padx=8)
        self.combo = ttk.Combobox(self, width=17 )# command=lambda x=self: self.update(x))  
        self.combo.bind("<<ComboboxSelected>>", self.combo_selected)
        self.combo['values'] =  values  #item['value_items'] #
        #self.combo.set(item['value'])
        #self.combo.current(1)  # установите вариант по умолчанию  
        self.combo.grid(row=1, column=0)


class RunAstraView(ttk.Frame):
    def __init__(self, master) -> None:
        super().__init__(master)        
        self.header_content =  { "title": "Run ASTRA", "buttons":[('Run calculation', self.start), ('Terminate', self.terminate), ('Test', None)]}
        self.astra_profiles = AstraBox.Models.AstraProfiles.default()
        self.hp = HeaderPanel(self, self.header_content)
        self.hp.grid(row=0, column=0, columnspan=5, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)
        self.columnconfigure(4, weight=1)        
        #self.rowconfigure(0, weight=1)    

        self.race_name = {'title': 'Race name', 'value': datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}
        self.rn_wdg = StringBox(self, self.race_name)
        self.rn_wdg.grid(row=1, column=0, columnspan=2, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)

        self.exp_combo = ComboBox(self, 'Experiments', Storage().exp_store.get_keys_list())
        self.exp_combo.grid(row=2, column=0, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)
        self.equ_combo = ComboBox(self, 'Equlibrium', Storage().equ_store.get_keys_list())
        self.equ_combo.grid(row=2, column=1, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)        
        self.rt_combo = ComboBox(self, 'RT configuration', Storage().rt_store.get_keys_list())
        self.rt_combo.grid(row=2, column=2, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)
        self.astra_combo = ComboBox(self, 'Astra profiles', Config.get_astra_profile_list())
        self.astra_combo.grid(row=2, column=3, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)

        runframe = ttk.LabelFrame(self,  text=f"Calculation log:")
        self.log_console = LogConsole(runframe)
        self.log_console.grid(row=1, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        runframe.columnconfigure(0, weight=1)
        runframe.rowconfigure(1, weight=1)
        self.first_init = True
        #self.bind('<Visibility>', self.visibilityChanged)
        runframe.grid(row=3, column=0, columnspan=5,  sticky=tk.N + tk.S + tk.E + tk.W)
        self.rowconfigure(3, weight=1)


    def start(self):
        #if self.grill_model == None:
        #    return
        #if self.imped_model == None:
        #    return
        exp = self.exp_combo.selected_value
        equ = self.equ_combo.selected_value
        rt = self.rt_combo.selected_value
        #name =  datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        race_model = RaceModel(name= self.race_name['value'], exp_name= exp, equ_name= equ, rt_name= rt ) 
        #self.controller.save_model(spectrum)
        astra_profile = Config.get_astra_profile(self.astra_combo.selected_value)
        self.worker = Kernel.AstraWorker(race_model, astra_profile)
        #self.worker.controller = self.controller
        self.log_console.set_logger(self.worker.logger)
        self.worker.on_progress = self.on_progress
        self.on_progress(0)
        self.worker.start()
        Storage().race_store.data[race_model.name] = race_model
        Storage().race_store.on_update_data()

    def terminate(self):
        pass

    def on_progress(self, pos):
        pass