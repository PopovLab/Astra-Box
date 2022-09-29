import os
import json
import pathlib 
from AstraBox.Models.BaseModel import BaseModel
from AstraBox.Storage import Storage

class RaceModel(BaseModel):

    def __init__(self, name = None, model= None) -> None:
        super().__init__(name, model)
        self._setting = None
        self.changed = False

    @property
    def model_name(self):
        return 'RaceModel'   

