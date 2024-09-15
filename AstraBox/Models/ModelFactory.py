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


def load(folder_item: WorkSpace.FolderItem):
    model = None
    p= folder_item.path
    if not p.exists():
        return None
    
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
    try:
        fi = content[model_name]
        return load(fi)
    except:
        return None

import uuid

def random_name():
    return 'new_'+str(uuid.uuid4())[0:4]

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

def model_dump_to_zip(zip, model, file_name):
    dump = model.model_dump_json(indent= 2)
    zip.writestr(file_name, dump)

def pack_model_to_zip(zip, model):
    if model:
        file_name = model.get_dest_path()        
        data = model.get_text()
        zip.writestr(file_name,data)


def make_folders(zip: ZipFile):
    for key, folder in Astra.data_folder.items():
        zip.mkdir(folder)


def prepare_task_zip(task:Task, zip_file):
    #zip_file = os.path.join(str(WorkSpace.get_location_path()), 'race_data.zip')
    #zip_file = WorkSpace.get_location_path().joinpath('race_data.zip')
    errors = []
    with ZipFile(zip_file, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel = 2) as zip:
        zip.comment = bytes(task.title,'UTF-8')
        make_folders(zip)

        model_dump_to_zip(zip, model= task, file_name='task.json')

        exp_model = get('ExpModel', task.exp)
        if exp_model is None:
            errors.append(f"ExpModel {task.exp} not exists")
            return errors


        equ_model =  get('EquModel', task.equ)
        if equ_model is None:
            errors.append(f"EquModel {task.equ} not exists")
            return errors
        
        pack_model_to_zip(zip, exp_model)
        pack_model_to_zip(zip, equ_model)


        models  = {
            'ExpModel' : exp_model.data,
            'EquModel' : equ_model.data,
            'name' : task.name
            }
        
        if task.rt is not None: # старая версия модели v1
            rt_model =  get('RTModel', task.rt)
            if rt_model:
                models['RTModel'] = rt_model.data
                pack_model_to_zip(zip, rt_model)
                pack_model_to_zip(zip, rt_model.get_spectrum_model())
                with zip.open( 'race_model.json' , "w" ) as json_file:
                    json_writer = encodings.utf_8.StreamWriter(json_file) 
                    # JSON spec literally fixes interchange encoding as UTF-8: https://datatracker.ietf.org/doc/html/rfc8259#section-8.1
                    json.dump(models, json_writer, ensure_ascii=False, indent=2)                
        elif task.frtc is not None: # новая версия v2
            frtc_model = get('FRTCModel', task.frtc)
            spectrum_model = get('SpectrumModel', task.spectrum)
            frtc_model.spectrum_kind = 'gauss_spectrum' #spectrum_model.spectrum.kind # нужно что бы знать тип спектра для файла конфигурации FRTC
            frtc_model.spectrum_PWM = spectrum_model.spectrum.PWM 
            pack_model_to_zip(zip, frtc_model)
            pack_model_to_zip(zip, spectrum_model)
            model_dump_to_zip(zip, model= frtc_model, file_name='frtc_model.json')
            model_dump_to_zip(zip, model= spectrum_model, file_name='spectrum_model.json')

        for key, item in WorkSpace.folder_content('SbrModel').items():
            pack_model_to_zip(zip, load(item))

            

    return errors
