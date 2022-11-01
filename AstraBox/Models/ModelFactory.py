import os
from pathlib import Path
import tkinter as tk

from AstraBox.Models.BaseModel import get_new_name
from AstraBox.Models.ExpModel import ExpModel
from AstraBox.Models.EquModel import EquModel
from AstraBox.Models.SbrModel import SbrModel
from AstraBox.Models.RTModel import RTModel
from AstraBox.Models.RaceModel import RaceModel
import AstraBox.WorkSpace as WorkSpace

def build(data_item):
    p = data_item.path
    print(p)
    print(p.suffix)
    match p.suffix:
        case '.exp':
            print(f'build exp - {p.name}')
            model = ExpModel(path= p)        
        case '.equ':
            print(f'build equ - {p.name}')
            model = EquModel(path= p)        
        case '.f':
            print(f'build sbr - {p.name}')
            model = SbrModel(path= p)        
        case '.json':
            print(f'build ray_tracing - {p.name}')
            model = RTModel(path= p )
        case '.zip':
            print(f'build race - {p.name}')
            model = RaceModel(path= p )            
        case _:
            print("Это другое")
            model = None
    return model    



def create_model(model_type, model_name=None, file=None):
    match model_type:
        case 'exp':
            print(f'create exp - {model_name}')
            model = ExpModel(model_name)        
        case 'equ':
            print(f'create equ - {model_name}')
            model = EquModel(model_name)        
        case 'sbr':
            print(f'create sbr - {model_name}')
            model = SbrModel(model_name)        
        case 'ray_tracing':
            print(f'create rt - {model_name}')
            ds = WorkSpace.getDataSource('ray_tracing')
            nn = get_new_name()
            path = ds.get_item_path(f'{nn}.json')
            model = RTModel(path= path)
        case _:
            print("Это другое")
            model = None
    return model


def delete_model(model)  -> bool:
    print(f'delete {model.name}')
    ans = tk.messagebox.askquestion(title="Warning", message=f'Delete {model.name}?', icon ='warning')
    if ans == 'yes':
        match model.model_name:
            case 'RaceModel':
                print('delete RaceModel')                 
                os.remove(model.race_zip_file)
                WorkSpace.getDataSource('races').refresh()
            case 'RTModel':
                print('delete RTModel')                 
                model.path.unlink()
                WorkSpace.getDataSource('ray_tracing').refresh()                
            case _:
                print('delete')
        return True
    return False


