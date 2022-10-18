import tkinter as tk
import os
import shelve
from sre_constants import NOT_LITERAL
import AstraBox.Models.ModelFactory as ModelFactory
import AstraBox.Config as Config

class ModelStore:
    def __init__(self, name) -> None:
        self.name = name
        self.on_update_data = None

    def close(self):
        self.data.close()

    def open(self, data_folder):
        self.data_folder = data_folder
        path = os.path.join(self.data_folder, self.name)
        if not os.path.exists(path):
            os.mkdir(path)

        filename = os.path.join(self.data_folder, f'{self.name}_db')
        self.data = shelve.open(filename)
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
            self.rt_store = ModelStore('rt')
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
        self.scan_folders()

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