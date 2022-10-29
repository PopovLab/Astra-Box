from pathlib import Path

import AstraBox.DataSource as DataSource

_instance = None

def getInstance():
    global _instance
    if _instance is None:
        _instance = WorkSpace()
    return _instance

class WorkSpace:
    def __init__(self) -> None:
        print('init workspace')
        self.DataSources = {}

    def open(self, path):
        print(f'Open {path}')
        self.destpath = Path(path)
        self.DataSources['exp'] = DataSource.build(path, 'exp')
        self.DataSources['equ'] = DataSource.build(path, 'equ')
        self.DataSources['sbr'] = DataSource.build(path, 'sbr')
        self.DataSources['ray_tracing'] = DataSource.build(path, 'ray_tracing')
        self.DataSources['races'] = DataSource.build(path, 'races')
        #print(self.DataSources['exp'].items())