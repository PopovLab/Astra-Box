from pathlib import Path

_location = None


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


def open(path):
    global _location
    print(f'Open {path}')
    _location = Path(path)
    for key, item in schema.items():
        item['binding'] = None
        refresh(key)
        

