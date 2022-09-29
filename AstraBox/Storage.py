import math
import os
import shelve
from sre_constants import NOT_LITERAL



class ModelStore:
    def __init__(self, name) -> None:
        self.name = name
        filename = os.path.join(Storage().data_folder, f'{name}_db')
        self.data = shelve.open(filename)

    def close(self):
        self.data.close()
    


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
        self.race_store = ModelStore('race')        

    def close(self):
        self.exp_store.close()
        self.equ_store.close()
        self.sbr_store.close()
        self.rt_store.close()        