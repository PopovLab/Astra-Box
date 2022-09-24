import os
import shelve
from AstraBox.Models.ExpModel import ExpModel

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
        db_filename = os.path.join(folder, 'db_shelve')
        self.data = shelve.open(db_filename)

        self.exp_store = ModelStore('exp')
        self.equ_store = ModelStore('equ')

        path = os.path.join(folder, 'exp')
        print(path)
        if os.path.exists(path):
            filenames = next(os.walk(path), (None, None, []))[2]
            for f in filenames:
                print(f)
                if not f in self.exp_store.data:
                    self.exp_store.data[f] = ExpModel(f)
        


    def close(self):
        self.exp_store.close()
        self.equ_store.close()