import encodings
import json
from zipfile import ZipFile
import zipfile

from returns.pipeline import is_successful
from returns.result import Failure

from AstraBox import Astra
from AstraBox.Models import ModelFactory
from AstraBox.Models.EquModel import EquModel
from AstraBox.Models.ExpModel import ExpModel
from AstraBox.WorkSpace import WorkSpace
from AstraBox.Task import Task

import traceback

def get_exception_traceback(e, num_frames=3):
    """
    Возвращает строку с информацией о последних num_frames фреймах
    в стеке вызовов, ведущем к исключению e.
    
    Если фреймов меньше, выводит все доступные.
    """
    # Получаем все фреймы трассировки (самый глубокий — последний)
    frames = traceback.extract_tb(e.__traceback__)
    print(len(frames))
    # Берём последние num_frames (или меньше)
    last_frames = frames[-num_frames:] if len(frames) >= num_frames else frames
    
    # Формируем строки для каждого фрейма
    lines = []
    for frame in last_frames:
        filename = frame.filename
        lineno = frame.lineno
        funcname = frame.name
        lines.append(f'  File "{filename}", line {lineno}, in {funcname}')
    
    # Возвращаем объединённую строку
    return "\n".join(lines)

def create_race_zip(work_space: WorkSpace, task: Task):
    print('create_race_zip')
    res = work_space.join_path('race_data.zip')
    if is_successful(res): 
        zip_file= res.unwrap()
        try :
            prepare_task_zip(work_space, task, zip_file)
        except Exception as e :
            #res = Failure(f"{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: \n{e}")
            # Получаем последние 3 фрейма трассировки
            trace_str = get_exception_traceback(e, num_frames=3)
            error_msg = f"{type(e).__name__}: {e}\nTraceback (most recent 3 calls):\n{trace_str}"
            res = Failure(error_msg)
    print(res)
    return res

        
def pack_model_to_zip(zip, model):
    if model:
        file_name = model.get_dest_path()        
        data = model.get_text()
        zip.writestr(file_name,data)

def make_folders(zip: ZipFile):
    for key, folder in Astra.data_folder.items():
        zip.mkdir(folder)

def model_dump_to_zip(zip, model, file_name):
    dump = model.model_dump_json(indent= 2)
    zip.writestr(file_name, dump)

def prepare_task_zip(work_space: WorkSpace, task: Task, zip_file):

    with ZipFile(zip_file, 'w', compression= zipfile.ZIP_DEFLATED, compresslevel = 2) as zip:
        zip.comment = bytes(task.title,'UTF-8')
        make_folders(zip)

        model_dump_to_zip(zip, model= task, file_name='task.json')

        exp_model = None
        folder = work_space.folder('ExpModel')
        for name, folder_item in folder.generator(task.exp):
            exp_model = ExpModel(path= folder_item.path)  
            pack_model_to_zip(zip, exp_model)
        #exp_model = get('ExpModel', task.exp)
        if exp_model is None:
            raise Exception(f"ExpModel {task.exp} not exists")

        equ_model = work_space.load_model(task.equ)
        zip.writestr(f"equ/{task.equ}", equ_model.text)            

        if task.rt is not None: # старая версия модели v1
            rt_model =  ModelFactory.get('RTModel', task.rt)
            if rt_model:
                models  = {
                'ExpModel' : exp_model.data,
                'EquModel' : equ_model.data,
                'name' : task.name
                }
                models['RTModel'] = rt_model.data
                pack_model_to_zip(zip, rt_model)
                pack_model_to_zip(zip, rt_model.get_spectrum_model())
                with zip.open( 'race_model.json' , "w" ) as json_file:
                    json_writer = encodings.utf_8.StreamWriter(json_file) 
                    # JSON spec literally fixes interchange encoding as UTF-8: https://datatracker.ietf.org/doc/html/rfc8259#section-8.1
                    json.dump(models, json_writer, ensure_ascii=False, indent=2)                
        else:# новая версия v2
            if task.frtc is None: 
                raise Exception(f"FRTC is not exists")
            if task.spectrum is None: 
                raise Exception(f"Spectrum is not exists")

            frtc_model = work_space.load_model(task.frtc)
            frtc_model.bind(lambda base: model_dump_to_zip(zip, model= base, file_name='frtc_model.json'))
            frtc_nml = frtc_model.bind(lambda base: base.export_to_nml())

            res = work_space.load_model(task.spectrum)
            if is_successful(res):
                spectrum_model = res.unwrap()
                model_dump_to_zip(zip, model= spectrum_model, file_name='spectrum_model.json')
                spm_nml = spectrum_model.export_to_nml()

                zip.writestr('lhcd/parameters.nml', f"{frtc_nml}\n{spm_nml}")
                print(spectrum_model)
                spectrum_data = work_space.load_spectrum_data(spectrum_model)
                spectrum_text = spectrum_data.bind(lambda base: spectrum_model.spectrum_data_to_text(base))
                if is_successful(spectrum_text):
                    zip.writestr('lhcd/spectrum.dat', spectrum_text.unwrap())
                else:
                    print(spectrum_text.failure())

        for key, item in work_space.folder_content('SbrModel').items():
            sbr_model = work_space.load_model(item.path)
            zip.writestr(f"sbr/{sbr_model.name}", sbr_model.text) 
            #pack_model_to_zip(zip, ModelFactory.load(item))

