import os
import json
import pathlib 
from AstraBox.Models.RootModel import RootModel

class EquModel():

    def __init__(self, name, data) -> None:
        self.name = name
        self.text = data
        self._setting = None
        self.changed = False

    @property
    def model_kind(self):
        return 'EquModel'   

    @classmethod
    def from_file(cls, file_path: pathlib.Path):
        """Создаёт модель из файла. Предполагается, что расширение соответствует классу."""
        with file_path.open('r') as f:
            data=  f.read()
        return cls(file_path.stem, data)

