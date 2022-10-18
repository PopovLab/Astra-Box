import uuid
import pathlib
import json

def get_uuid_id():
    return str(uuid.uuid4())

class BaseModel:
    
    def __init__(self, name = None) -> None:
        self.data = {}
        if name is None:
            self.data['name'] = 'undef_' + get_uuid_id()[0:4]
        else:
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

    @property
    def uuid(self):
        return self.data['uuid']

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