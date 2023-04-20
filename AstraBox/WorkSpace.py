from pathlib import Path

import AstraBox.DataSource as DataSource

_instance = None

def getInstance():
    global _instance
    if _instance is None:
        _instance = WorkSpace()
    return _instance

def getDataSource(data_source):
    return getInstance().DataSources[data_source]
    

def get_location_path(data_source = None):
    """get workspace location path"""
    if data_source:
        ds = getInstance().DataSources[data_source]
        print(ds.destpath)
        return ds.destpath
    else:
        return getInstance().location

def refresh(name):
    ds = getDataSource(name)
    ds.refresh()

def get_item_list(name):
    return getDataSource(name).get_keys_list()

def get_item_location(model_kind, model_name):
    loc = get_location_path()
    return Path(loc).joinpath(model_name)

def refresh2(name):
    obj = schema[name].get('binding')
    if obj:  obj.refersh()

def set_binding(name, object):
    schema[name]['binding'] = object

def get_title(name):
    return schema[name]['title']

def get_shema(model_kind):
    return schema[model_kind]

catalog = {}

def get_models_dict(model_kind):
    global catalog
    if model_kind not in catalog:
        loc = schema[model_kind]['location']
        destpath = get_location_path().joinpath(loc)
        catalog[model_kind] = {p.name: p for p in destpath.glob('*.*')}
    return catalog[model_kind]

schema = {
    "ExpModel"  : {
        'title'   : 'Experiments xyz',
        'location': 'exp',
        'binding' : None
    },
    "EquModel"  : {
        'title'   : 'Equlibrium',
        'location': 'equ',
        'binding' : None
    },
    "SbrModel"  : {
        'title'   : 'Subroutine',
        'location': 'sbr',
        'binding' : None
    },
    "RTModel"   : {
        'title'   : 'Ray Tracing Configurations',
        'location': 'ray_tracing',
        'new_btn' : True,
        'binding' : None
    },
    "RaceModel" : {
        'title'   : 'Race history',
        'location': 'races',
        'binding' : None,
        'reverse_sort' : True
    }
}

class WorkSpace:
    def __init__(self) -> None:
        print('init workspace')
        self.DataSources = {}
        for key in ['exp', 'equ', 'sbr', 'ray_tracing', 'races']:
            self.DataSources[key] = DataSource.DataSource(key)

    def open(self, path):
        print(f'Open {path}')
        self.location = Path(path)
        for key, ds in self.DataSources.items():
            ds.open(self.location)
        

