import uuid
import os
import pathlib
import json

def get_uuid_id():
    return str(uuid.uuid4())

class BaseModel:
    def __init__(self, name = None) -> None:
        self.data = {}
        if name:
            self.data['name'] = name

    @property
    def name(self):
        return self.data['name']

    @name.setter
    def name(self, value):
        self.data['name'] = value

    @property
    def model_name(self):
        return 'BaseModel'

    def read(self, folder= None, path= None):
        f = os.path.join(folder, f'{self.name}.json')
        if path:
            f = str(path)
        with open(f, "r") as json_file:
            self.data = json.load(json_file)

    def write(self, folder= None):
        f = os.path.join(folder, f'{self.name}.json')
        with open(f, "w") as json_file:
            json.dump(self.data, json_file, indent=2)

    @property
    def status(self):
        value = self.data.get('status')
        if value:
            return value
        else:
            return ''

    @status.setter
    def status(self, value):
        self.data['status'] = value

    @property
    def version(self):
        value = self.data.get('version')
        if value:
            return value
        else:
            return ''

    @version.setter
    def version(self, value):
        self.data['version'] = value        