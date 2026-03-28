import os
import json
import pathlib 
from AstraBox.Models.RootModel import RootModel

class SbrModel():

    def __init__(self,  name, data) -> None:
        self.name = name
        self.text = data
        self._setting = None
        self.changed = False
        self._setting = None
        self.changed = False

    @property
    def model_kind(self):
        return 'SbrModel'   

    @classmethod
    def from_file(cls, file_path: pathlib.Path):
        """Создаёт модель из файла. Предполагается, что расширение соответствует классу."""
        with file_path.open('r') as f:
            data=  f.read()
        return cls(file_path.name, data)

    def save_to_file(self, path):
        #print(f'encoding {self.encoding}')
        with path.open(mode='w') as f:
            f.write(self.text)