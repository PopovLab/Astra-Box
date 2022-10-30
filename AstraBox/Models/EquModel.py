import os
import json
import pathlib 
from AstraBox.Models.BaseModel import BaseModel

class EquModel(BaseModel):

    def __init__(self, name= None, path= None) -> None:
        if name:
            super().__init__(name)
        if path:
            super().__init__(path.name)
            self._path = path
        self._setting = None
        self.changed = False

    @property
    def model_name(self):
        return 'EquModel'   

    def get_text(self):
        path = str(self._path) #os.path.join(Storage().data_folder, 'equ', self.name)
        print(path)
        with open(path) as f:
            lines = f.read()

        return lines        

    def save_text(self, text):
        path = str(self._path) #os.path.join(Storage().data_folder, 'equ', self.name)
        with open(path, mode='w') as f:
            f.write(text)

    def get_dest_path(self):
        return os.path.join('equ', self.name)        