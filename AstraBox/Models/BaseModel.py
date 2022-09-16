import uuid
import pathlib
import json

def get_uuid_id():
    return str(uuid.uuid4())

class BaseModel:
    
    def __init__(self, name = None, model = None) -> None:
        self.data = {}
        if model is not None:
            self.data = model.data.copy()
            self.data['uuid'] = get_uuid_id()
            self.data['name'] = model.name + '_' + self.data['uuid'][0:4]
            self.status = ''
            return

        self.data['uuid'] = get_uuid_id()
        if name is None:
            self.data['name'] = 'undef_' + self.data['uuid'][0:4]
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