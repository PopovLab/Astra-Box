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
    _items = None    
    on_refresh = None

    def __init__(self, destpath='.') -> None:
        self.destpath = Path(destpath)
        pass
    
    @property
    def items(self):
        if self._items is None:
            return self.get_items()
        return self._items
    
    def get_keys_list(self):
        return list(self.items.keys())        

    def get_items(self):
        self._items = {p.name: DataItem(p) for p in self.destpath.glob('*.*')}
        return self._items

    def refresh(self):
        if self.on_refresh:
            self.on_refresh()


