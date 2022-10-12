import os
import json
import pathlib 
from AstraBox.Models.BaseModel import BaseModel
from AstraBox.Storage import Storage

class ExpModel(BaseModel):

    def __init__(self, name = None, model= None) -> None:
        super().__init__(name, model)
        self._setting = None
        self.changed = False

    @property
    def model_name(self):
        return 'ExpModel'

    def get_text(self):
        path = os.path.join(Storage().data_folder, 'exp', self.name)
        print(path)
        with open(path) as f:
            lines = f.read()
        return lines

    def save_text(self, text):
        path = os.path.join(Storage().data_folder, 'exp', self.name)
        with open(path, mode='w') as f:
            f.write(text)

    def get_dest_path(self):
        return os.path.join('exp', self.name)