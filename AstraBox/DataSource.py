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

    def __init__(self, name) -> None:
        self.name = name
        pass
    
    def open(self, destpath='.') -> None:
        self.destpath = Path(destpath).joinpath(self.name)
        if not self.destpath.exists():
            self.destpath.mkdir()
        self.get_items()
        self.refresh()

    @property
    def items(self):
        if self._items is None:
            return self.get_items()
        return self._items
    
    def get_keys_list(self):
        return list(self.items.keys())        

    def get_item_path(self, name):
        return self.destpath.joinpath(name)

    def get_items(self):
        self._items = {p.name: DataItem(p) for p in self.destpath.glob('*.*')}
        return self._items

    def refresh(self):
        if self.on_refresh:
            self.on_refresh()


