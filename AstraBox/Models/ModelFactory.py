import os
from pathlib import Path
import tkinter as tk

from AstraBox.Models.RootModel import get_new_name
from AstraBox.Models.ExpModel import ExpModel
from AstraBox.Models.EquModel import EquModel
from AstraBox.Models.SbrModel import SbrModel
from AstraBox.Models.RTModel import RTModel
from AstraBox.Models.RaceModel import RaceModel
import AstraBox.WorkSpace as WorkSpace

def do(action:dict):
    print(action)
    model = None
    match action['action']:
        case 'new_model':
            model = create_model(action['model_kind'])
        case 'show':
            model = load(action['data'].path)
    return model

def build(data_item):
    p = data_item.path
    print(p)
    print(p.suffix)
    return load(p)

def load(p):
    match p.suffix:
        case '.exp':
            print(f'build exp - {p.name}')
            model = ExpModel(path= p)        
        case '.equ':
            print(f'build equ - {p.name}')
            model = EquModel(path= p)        
        case '.f' | '.f90':
            print(f'build sbr - {p.name}')
            model = SbrModel(path= p)        
        case '.rt':
            print(f'build ray_tracing - {p.name}')
            model = RTModel(path= p )
        case '.zip':
            print(f'build race - {p.name}')
            model = RaceModel(path= p )            
        case _:
            print("Это другое")
            model = None
    return model 

def get(model_kind= None, model_name= None):
    d = WorkSpace.get_models_dict(model_kind)
    try:
        vi = d[model_name]
        return load(vi.path)
    except:
        return None

def create_model(model_kind=None ):
    match model_kind:
        case 'exp':
            print(f'create exp - {model_kind}')
            model = ExpModel(model_kind)        
        case 'equ':
            print(f'create equ - {model_kind}')
            model = EquModel(model_kind)        
        case 'sbr':
            print(f'create sbr - {model_kind}')
            model = SbrModel(model_kind)        
        case 'RTModel':
            print(f'create rt - {model_kind}')
            p = WorkSpace.get_location_path('RTModel')
            path = p.joinpath(f'{get_new_name()}.rt')
            model = RTModel(path= path)
        case _:
            print("Это другое")
            model = None
    return model


def delete_model(model)  -> bool:
    print(f'try delete {model.name}')
    ans = tk.messagebox.askquestion(title="Warning", message=f'Delete {model.name}?', icon ='warning')
    deleted = False
    if ans == 'yes':
        match model.model_kind:
            case 'RaceModel':
                os.remove(model.race_zip_file)
                WorkSpace.refresh('RaceModel')
                deleted = True

            case 'RTModel':
                model.path.unlink()
                WorkSpace.refresh('RTModel')                
                deleted = True

            case 'ExpModel':
                model.path.unlink()
                WorkSpace.refresh('ExpModel')                
                deleted = True   

            case 'EquModel':
                model.path.unlink()
                WorkSpace.refresh('EquModel')                
                deleted = True   

            case 'SbrModel':
                model.path.unlink()
                WorkSpace.refresh('SbrModel')                
                deleted = True                
            case _:

                print('delete')

    return deleted



