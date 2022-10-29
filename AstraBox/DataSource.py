import os
from pathlib import Path

def build(parent_path, path):
    full = os.path.join(parent_path, path)
    return DataSource(full)

class DataItem():
    def __init__(self, p) -> None:
        self.title = p.stem
        self.path = p
        pass

class DataSource:
    def __init__(self, destpath='.') -> None:
        self.destpath = Path(destpath)
        pass
    
    def get_items(self):
        return list(DataItem(p) for p in self.destpath.glob('*.*'))
