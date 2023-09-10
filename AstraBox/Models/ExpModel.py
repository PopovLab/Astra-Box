import os
import json
import pathlib 
from AstraBox.Models.BaseModel import BaseModel

class ExpModel(BaseModel):

    def __init__(self, name= None, path= None) -> None:
        if name:
            super().__init__(name)
        if path:
            super().__init__(path.stem)
            self.path = path
        self._setting = None
        self.changed = False


    @property
    def model_kind(self):
        return 'ExpModel'


    def get_dest_path(self):
        return os.path.join('exp', self.path.name)
    

    def parsing_source(self):
        pass