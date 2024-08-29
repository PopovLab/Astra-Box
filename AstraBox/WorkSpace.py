import tkinter as tk
from pathlib import Path
from pydantic import BaseModel, Field

_location = None

#import AstraBox.WorkSpace as WorkSpace

def get_location_path(model_kind = None):
    """get workspace location path"""
    if model_kind:
        loc = _location.joinpath(schema[model_kind]['location'])
        if not loc.exists():
            print(f"make dir {loc}")
            loc.mkdir()
        return loc
    else:
        return _location

def temp_folder_location():
    loc = get_location_path().joinpath('tmp')
    if not loc.exists():
        print(f"make dir {loc}")
        loc.mkdir()
    return loc

def get_item_location(model_kind, model_name):
    loc = get_location_path()
    return Path(loc).joinpath(model_name)

def refresh(model_kind):
    if model_kind in catalog:
        del catalog[model_kind]
    obj = schema[model_kind].get('binding')
    if obj:  obj.refresh()

def set_binding(name, object):
    schema[name]['binding'] = object

def get_title(name):
    return schema[name]['title']

def get_shema(model_kind):
    return schema[model_kind]

catalog = {}

def __get_item_list(model_kind):
    return list(__get_models_dict(model_kind).keys())

import zipfile

def __get_models_dict(model_kind):
    global catalog
    if _location:
        if model_kind not in catalog:
            loc = schema[model_kind]['location']
            destpath = get_location_path().joinpath(loc)
            catalog[model_kind] = {} #{p.name: FolderItem(p.name, p, 'comment', model_kind) for p in destpath.glob('*.*') if p.name !='.gitignore'}
    else:
        catalog[model_kind] = None
    return catalog[model_kind]


class FolderItem():
    def __init__(self, folder,  path:Path) -> None:
        self.parent = folder
        self.name= path.name
        self.path= path
        self.comment= ''
        self.model_kind= folder.content_type
        self.on_update= None
        match path.suffix:
            case '.zip':
                with zipfile.ZipFile(path) as zip:
                    self.comment = zip.comment.decode("utf-8")           
            case _:
                self.comment= ''

    def remove(self)->bool:
        return self.parent.remove(self)

class Folder(BaseModel):
    title: str
    content_type: str
    required: bool = True
    location: str
    sort_direction: str=  'default'
    tag: str = 'top'
    _root: str
    _observers = set()

    
    def attach(self, observer):
        if (observer not in self._observers):
            self._observers.add(observer)

    def detach(self, observer):
        if (observer in self._observers):
            self.observers.remove(observer)
        
    def raise_event(self, event_name):
        print(event_name)
        for event_observer in self._observers:
            event_observer(event_name)

    def exists(self, root_path)->bool:
        self._location = root_path.joinpath(self.location)
        if self._location.exists():
            return True
        else:
            if self.required:
                print(f"make dir {self._location}")
                self._location.mkdir()
                return True
        return False
    
    def populate(self):
        self._content = {p.name: FolderItem(self, p) for p in self._location.glob('*.*') if p.name !='.gitignore'}

    def remove(self, item)->bool:
        print(f'remove {item.name}')
        ans = tk.messagebox.askquestion(title="Warning", message=f'Delete {item.name}?', icon ='warning')
        removed = False
        if ans == 'yes':
            self._content.pop(item.name, None)
            self.raise_event('itemsRemoved')
            removed= True
        return removed
    


default_catalog = [
    Folder(title= 'Experiments', content_type='ExpModel', location= 'exp'),
    Folder(title= 'Equlibrium', content_type='EquModel', location= 'equ'),
    Folder(title= 'Subroutine', content_type='SbrModel', location= 'sbr'),
    Folder(title= 'Ray Tracing Configurations', content_type='RTModel', location= 'ray_tracing', required= False),
    Folder(title= 'Race history', content_type='RaceModel', location= 'races', sort_direction= 'reverse', tag= 'bottom'),
]

class WorkSpace(BaseModel):
    folders: list[Folder] = []
    _location: str


    def open(self, path):
        self._location = Path(path)
        for folder in default_catalog:
            if folder.exists(self._location):
                folder.populate()
                self.folders.append(folder)

    def print(self):
        for folder in self.folders:
            print('------')
            print(folder)
            for x in folder._content:
                print(x)

    def folder_content(self, content_type):
        matches = [x for x in self.folders if x.content_type == content_type]
        if len(matches)>0:
            return matches[0]._content
        else:
            return None

    def get_folder_content(self, content_type):
        content = self.folder_content(content_type)
        if content:
            return list(content.keys())
        else:
            return []

schema = {
    "ExpModel"  : {
        'title'   : 'Experiments',
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
        #'new_btn' : True,
        'binding' : None
    },
    "RaceModel" : {
        'title'   : 'Race history',
        'location': 'races',
        'binding' : None,
        'reverse_sort' : True
    }
}

work_space = None
def get_folder_content(content_type):
    if work_space:
        return work_space.get_folder_content(content_type)

def folder_content(content_type):
    if work_space:
        return work_space.folder_content(content_type)
        
def open(path):
    global _location
    global work_space
    print(f'Open {path}')
    work_space = WorkSpace()
    work_space.open(path)
    #work_space.print()

    _location = Path(path)
    for key, item in schema.items():
        item['binding'] = None
        refresh(key)
    return work_space

