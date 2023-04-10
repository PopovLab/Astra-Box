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
        return ds.destpath
    else:
        return getInstance().location

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
        

   