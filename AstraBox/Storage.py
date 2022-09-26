import math
import os
import shelve
from sre_constants import NOT_LITERAL
from AstraBox.Models.ExpModel import ExpModel
from AstraBox.Models.EquModel import EquModel
from AstraBox.Models.SbrModel import SbrModel
from AstraBox.Models.RTModel import RTModel

class ModelStore:
    def __init__(self, name) -> None:
        self.name = name
        filename = os.path.join(Storage().data_folder, f'{name}_db')
        self.data = shelve.open(filename)

    def close(self):
        self.data.close()
    
    def create_model(self):
        match self.name:
            case 'rt':
                print(f'create {self.name} model')
                model = RTModel('new model')
            case _:
                print("Это другое")
                model = None

        return model

class Storage:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Storage, cls).__new__(cls)
        return cls.instance
        
    def __init__(self) -> None:
        print('Storage.init')
        #self.data = None

    def open(self, folder) ->None:
        self.data_folder = folder

        self.exp_store = ModelStore('exp')
        self.equ_store = ModelStore('equ')
        self.sbr_store = ModelStore('sbr')
        self.rt_store = ModelStore('rt')

        path = os.path.join(folder, 'exp')
        if os.path.exists(path):
            filenames = next(os.walk(path), (None, None, []))[2]
            for f in filenames:
                if not f in self.exp_store.data:
                    self.exp_store.data[f] = ExpModel(f)

        path = os.path.join(folder, 'equ')
        if os.path.exists(path):
            filenames = next(os.walk(path), (None, None, []))[2]
            for f in filenames:
                if not f in self.equ_store.data:
                    self.equ_store.data[f] = EquModel(f)        

        path = os.path.join(folder, 'sbr')
        if os.path.exists(path):
            filenames = next(os.walk(path), (None, None, []))[2]
            for f in filenames:
                if not f in self.sbr_store.data:
                    self.sbr_store.data[f] = SbrModel(f)   



    def close(self):
        self.exp_store.close()
        self.equ_store.close()
        self.sbr_store.close()
        self.rt_store.close()        