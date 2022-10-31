import os
import json
import pathlib 
from AstraBox.Models.BaseModel import BaseModel

class SbrModel(BaseModel):

    def __init__(self, name = None, path= None) -> None:
        if name:
            super().__init__(name)
        if path:
            super().__init__(path.name)
            self.path = path
        self._setting = None
        self.changed = False

    @property
    def model_name(self):
        return 'SbrModel'   

    def get_dest_path(self):
        return os.path.join('sbr', self.name)