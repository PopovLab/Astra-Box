import os
import json
import re 

__instance = {
        'current_workspace_dir' : 'data'
    }


def get():
    global __instance
    abspath = os.path.join(os.path.abspath('data'), 'config.json')
    if os.path.exists(abspath):
        with open(abspath) as json_file:
            __instance = json.load(json_file)
    return __instance

def save():
    global __instance
    abspath = os.path.join(os.path.abspath('data'), 'config.json')
    with open( abspath , "w" ) as json_file:
        json.dump( __instance , json_file, indent = 2 )

def get_current_workspace_dir():
    return get()['current_workspace_dir']

def set_current_workspace_dir(path):
    global __instance
    print(f'set workspace: {path}')
    __instance['current_workspace_dir'] = path
    save()
