import os
import json
import pathlib 
from AstraBox.Models.BaseModel import BaseModel

class SbrModel(BaseModel):

    def __init__(self, name = None, model= None) -> None:
        super().__init__(name, model)
        self._setting = None
        self.changed = False

    @property
    def model_name(self):
        return 'SbrModel'   