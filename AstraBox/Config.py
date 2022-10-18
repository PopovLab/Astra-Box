import os
import json
import re 

__instance = {
        'CWD' : 'data'
    }


def get_cfg():
    global __instance
    abspath = os.path.join(os.path.abspath('data'), 'config.json')
    if os.path.exists(abspath):
        with open(abspath) as json_file:
            __instance = json.load(json_file)
    return __instance

def save_cfg():
    global __instance
    abspath = os.path.join(os.path.abspath('data'), 'config.json')
    with open( abspath , "w" ) as json_file:
        json.dump( __instance , json_file, indent = 2 )

def get_CWD():
    return get_cfg()['CWD']

def set_CWD(path):
    global __instance
    print(f'set CWD: {path}')
    __instance['CWD'] = path
    save_cfg()
