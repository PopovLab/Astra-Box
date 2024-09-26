import uuid
import os
import pathlib
import json

def get_uuid_id():
    return str(uuid.uuid4())

def get_new_name():
    return f'new_model_{get_uuid_id()[0:4]}'

class RootModel:
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
    def model_kind(self):
        return 'RootModel'

    def try_decode(self, data:bytearray):
        for encoding in ['utf-8', 'ascii', 'cp866']:
            try:
                lines = data.decode(encoding)
                break
            except UnicodeDecodeError as e:
                print(f"{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: \n{e}")
        print(f'good encoding {encoding}')
        return lines

    def get_text(self):
        with self.path.open('rb') as f:
            rawdata = f.read()
        return self.try_decode(rawdata)

    def save_text(self, text):
        with self.path.open(mode='w', encoding='utf-8') as f:
            f.write(text)

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