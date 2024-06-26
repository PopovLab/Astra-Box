import os
import json
import re 

__instance = {
        'Astra Profiles':{
            "Astra-6 a4": {
                'home' : '/home/tmp8/ASTRA-6',
                'profile' : 'a4',
                'dest' : '\\\\wsl$\\Ubuntu-20.04\\home\\tmp8\\ASTRA-6'
            },
            "Astra-7 a3": {
                'home' : '/home/tmp8/ASTRA-7',
                'profile' : 'a3',
                'dest' : '//wsl$/Ubuntu-20.04/home/tmp8/ASTRA-7',
            },        
        }
    }
def get_config_path():
    return os.path.join(os.path.abspath('data'), 'config.json')

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


def get_astra_profile_list():
    cfg = get()
    return list(cfg['Astra Profiles'].keys())

def get_astra_profile(profile_name):
    cfg = get()
    return cfg['Astra Profiles'][profile_name]