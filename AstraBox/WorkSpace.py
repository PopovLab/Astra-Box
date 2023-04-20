from pathlib import Path

_location = None


def get_location_path(model_kind = None):
    """get workspace location path"""
    if model_kind:
        loc = _location.joinpath(schema[model_kind]['location'])
        print(loc)
        return loc
    else:
        return _location



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


def open(path):
    global _location
    print(f'Open {path}')
    _location = Path(path)
    for key, _ in schema.items():
        refresh(key)
        

