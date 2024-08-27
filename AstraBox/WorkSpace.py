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

def get_item_list(model_kind):
    return list(get_models_dict(model_kind).keys())

import zipfile

class ViewItem():
    def __init__(self, name:str, path:Path, comment:str, model_kind:str) -> None:
        self.name= name
        self.path= path
        self.comment= ''
        self.model_kind= model_kind
        self.on_update= None
        match path.suffix:
            case '.zip':
                with zipfile.ZipFile(path) as zip:
                    self.comment = zip.comment.decode("utf-8")           
            case _:
                self.comment= ''

def get_models_dict(model_kind):
    global catalog
    if _location:
        if model_kind not in catalog:
            loc = schema[model_kind]['location']
            destpath = get_location_path().joinpath(loc)
            catalog[model_kind] = {p.name: ViewItem(p.name, p, 'comment', model_kind) for p in destpath.glob('*.*') if p.name !='.gitignore'}
    else:
        catalog[model_kind] = None
    return catalog[model_kind]


class Folder(BaseModel):
    title: str
    model_kind: str
    required: bool = True
    location: str
    sort_direction: str=  'default'
    tag: str = 'top'
    _root: str
    #_content: list[str] = []

    def exists(self, root_path)->bool:
        self._location = root_path.joinpath(self.location)
        if self._location.exists():
            return True
        else:
            if self.required:
                print(f"make dir {self._location}")
                self._location.mkdir()
        return True
    
    def populate(self):
        self._content = {p.name: ViewItem(p.name, p, 'comment', self.model_kind) for p in self._location.glob('*.*') if p.name !='.gitignore'}

default_catalog = [
    Folder(title= 'Experiments', model_kind='ExpModel', location= 'exp'),
    Folder(title= 'Equlibrium', model_kind='EquModel', location= 'equ'),
    Folder(title= 'Subroutine', model_kind='SbrModel', location= 'sbr'),
    Folder(title= 'Ray Tracing Configurations', model_kind='RTModel', location= 'ray_tracing', required= False),
    Folder(title= 'Race history', model_kind='RaceModel', location= 'races', sort_direction= 'reverse', tag= 'bottom'),
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
def open(path):
    global _location
    global work_space
    print(f'Open {path}')
    work_space = WorkSpace()
    work_space.open(path)
    work_space.print()

    _location = Path(path)
    for key, item in schema.items():
        item['binding'] = None
        refresh(key)
    return work_space

