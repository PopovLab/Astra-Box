import tkinter as tk
import os
import shelve
from sre_constants import NOT_LITERAL
import AstraBox.Models.ModelFactory as ModelFactory
import AstraBox.Config as Config

class ModelStore:
    def __init__(self, model_type) -> None:
        self.model_type = model_type
        self.data = {}
        self.on_update_data = None

    def close(self):
        self.data.close()

    def reset(self, data_folder):
        self.data_folder = data_folder
        self.data = {}
        if self.on_update_data:
            self.on_update_data()        

    def open(self, data_folder):
        self.data_folder = data_folder
        self.model_folder = os.path.join(self.data_folder, self.model_type)
        if not os.path.exists(self.model_folder):
            os.mkdir(self.model_folder)
        self.data = {}
        self.scan_folder()
        #filename = os.path.join(self.data_folder, f'{self.name}_db')
        #self.data = shelve.open(filename)
        if self.on_update_data:
            self.on_update_data()        

    def scan_folder(self):
        if os.path.exists(self.model_folder):
            filenames = next(os.walk(self.model_folder), (None, None, []))[2]
            for f in filenames:
                print(f)
                if not f in self.data:
                    self.data[f] = ModelFactory.create_model(self.model_type, f)

    def save_model(self, model):
        self.data[model.name] = model
        model.write(self.model_folder)
        self.update()

    def update(self):
        if self.on_update_data:
            self.on_update_data()  

    def get_keys_list(self):
        return list(self.data.keys())
    
    def delete_model(self, key):
        del self.data[key]
        if self.on_update_data:
            self.on_update_data()

class Storage:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            print('new instance')
            cls.instance = super(Storage, cls).__new__(cls)
        return cls.instance

    __init_flag__ = True    
    tk_root = None

    def __init__(self) -> None:
        print('Storage.init')
        if self.__init_flag__:
            self.exp_store = ModelStore('exp')
            self.equ_store = ModelStore('equ')
            self.sbr_store = ModelStore('sbr')
            self.rt_store = ModelStore('ray_tracing')
            self.race_store = ModelStore('races')            
            
            self.__init_flag__ = False

    def open(self, folder) ->None:
        print(folder)
        self.tk_root.title(f"ASTRA Box in {folder}")
        Config.set_current_workspace_dir(folder)
        self.data_folder = folder

        self.exp_store.open(folder)
        self.equ_store.open(folder)
        self.sbr_store.open(folder)
        self.rt_store.open(folder)
        self.race_store.open(folder)         
        #self.scan_folders()
        #self.exp_store.update()
        #self.equ_store.update()
        #self.sbr_store.update()

    def close(self):
        self.exp_store.close()
        self.equ_store.close()
        self.sbr_store.close()
        self.rt_store.close()        


    def scan_folders(self):
        
        path = os.path.join(self.data_folder, 'exp')
        if os.path.exists(path):
            filenames = next(os.walk(path), (None, None, []))[2]
            for f in filenames:
                if not f in self.exp_store.data:
                    self.exp_store.data[f] = ModelFactory.create_model('exp',f)

        path = os.path.join(self.data_folder, 'equ')
        if os.path.exists(path):
            filenames = next(os.walk(path), (None, None, []))[2]
            for f in filenames:
                if not f in self.equ_store.data:
                    self.equ_store.data[f] = ModelFactory.create_model('equ',f)     

        path = os.path.join(self.data_folder, 'sbr')
        if os.path.exists(path):
            filenames = next(os.walk(path), (None, None, []))[2]
            for f in filenames:
                if not f in self.sbr_store.data:
                    self.sbr_store.data[f] = ModelFactory.create_model('sbr',f)               