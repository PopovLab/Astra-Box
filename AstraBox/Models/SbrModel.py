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

    @classmethod
    def from_file(cls, file_path: pathlib.Path):
        """Создаёт модель из файла."""
        data = file_path.read_text(encoding='utf-8')
        return cls(file_path.name, data)

    def save_to_file(self, path):
        #print(f'encoding {self.encoding}')
        with path.open(mode='w', encoding='utf-8') as f:
            f.write(self.text)