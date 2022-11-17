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
            path = ds.get_item_path(f'{get_new_name()}.rt')
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
        match model.model_name:
            case 'RaceModel':
                os.remove(model.race_zip_file)
                WorkSpace.getDataSource('races').refresh()
                deleted = True

            case 'RTModel':
                model.path.unlink()
                WorkSpace.getDataSource('ray_tracing').refresh()                
                deleted = True

            case 'ExpModel':
                model.path.unlink()
                WorkSpace.getDataSource('exp').refresh()                
                deleted = True   

            case 'EquModel':
                model.path.unlink()
                WorkSpace.getDataSource('equ').refresh()                
                deleted = True   

            case 'SbrModel':
                model.path.unlink()
                WorkSpace.getDataSource('sbr').refresh()                
                deleted = True                
            case _:

                print('delete')

    return deleted



def refresh(model)  -> None:
    print(f'refresh {model.name}')
    match model.model_name:
        case 'RaceModel':
            WorkSpace.getDataSource('races').refresh()

        case 'RTModel':
            WorkSpace.getDataSource('ray_tracing').refresh()                

        case 'ExpModel':
            WorkSpace.getDataSource('exp').refresh()                

        case 'EquModel':
            WorkSpace.getDataSource('equ').refresh()                
        case 'SbrModel':
            WorkSpace.getDataSource('sbr').refresh()                
        case _:
            pass

