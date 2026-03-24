import os
from pathlib import Path
import tkinter as tk
from zipfile import ZipFile
import zipfile

from AstraBox import Astra
from AstraBox.Models.RootModel import get_new_name
from AstraBox.Models.ExpModel import ExpModel
from AstraBox.Models.EquModel import EquModel
from AstraBox.Models.SbrModel import SbrModel
from AstraBox.Models.RTModel import RTModel
from AstraBox.Models.RaceModel import RaceModel
from AstraBox.Models.FRTCModel import FRTCModel
from AstraBox.Task import Task
import AstraBox.Models.SpectrumModel_v2 as SpectrumModel_v2
import AstraBox.WorkSpace as WorkSpace

def load_model(file_path):
    """Загружает модель из файла, определяя тип по расширению."""
    if not file_path.exists():
        raise FileNotFoundError(f"{p} was not found")
    ext = file_path.suffix
    models = {
        '.exp': ExpModel,
        '.equ': EquModel,
        '.sbr': SbrModel,
        '.rt': RTModel,
    }
    if ext not in models:
        raise ValueError(f"Неподдерживаемое расширение: .{ext}")
    return models[file_path.suffix].from_file(file_path)

def load(folder_item: WorkSpace.FolderItem):
    model = None
    p= folder_item.path
    if not p.exists():
        raise FileNotFoundError(f"{p} was not found")
    
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

        case '.frtc':
            print(f'load frtc - {p.name}')
            with open(p, encoding='utf-8') as file:
                    dump = file.read()
            model = FRTCModel.construct(dump)
        case '.spm':
            print(f'load spm - {p.name}')
            with open(p, encoding='utf-8') as file:
                    dump = file.read()
            print(dump)
            model = SpectrumModel_v2.SpectrumModel.construct(dump)            
            print(model)
        case '.zip':
            print(f'build race - {p.name}')
            model = RaceModel(path= p )            
        case _:
            print("Это другое")
            model = None
    return model 

def get(model_kind= None, model_name= None):
    content = WorkSpace.folder_content(model_kind)
    if content is None:
        return None

    fi = content[model_name]
    return load(fi)


def get2(model_kind= None, model_name= None):
    folder = WorkSpace.folder(model_kind)
    content = folder.generator(model_name)
    for name, folder_item in content:
        yield load(folder_item)



import uuid

def random_name():
    return 'new_' + str(uuid.uuid4())[0:4]

def create_spectrum_model(spectrum_type):
    model = None
    print(f'create specturm: {spectrum_type}')
    model = SpectrumModel_v2.SpectrumModel.construct_new(random_name(), spectrum_type)
    return model

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
        case 'FRTCModel':
            print(f'create rt - {model_kind}')
            model = FRTCModel(name=random_name())
        case _:
            print("Это другое")
            model = None
    return model

def clone_model(model):
    model.name= model.name + '_clone_' + str(uuid.uuid4())[0:4]
    return model

def delete_model(model)  -> bool:
    print(f'try delete {model.name}')
    ans = tk.messagebox.askquestion(title="Warning", message=f'Delete {model.name}?', icon ='warning')
    deleted = False
    if ans == 'yes':
        match model.model_kind:
            case 'RaceModel':
                os.remove(model.race_zip_file)
                WorkSpace.refresh_folder('RaceModel')
                deleted = True

            case 'RTModel':
                model.path.unlink()
                WorkSpace.refresh_folder('RTModel')                
                deleted = True

            case 'ExpModel':
                model.path.unlink()
                WorkSpace.refresh_folder('ExpModel')                
                deleted = True   

            case 'EquModel':
                model.path.unlink()
                WorkSpace.refresh_folder('EquModel')                
                deleted = True   

            case 'SbrModel':
                model.path.unlink()
                WorkSpace.refresh_folder('SbrModel')                
                deleted = True                
            case _:

                print('delete')

    return deleted


import json
import encodings


