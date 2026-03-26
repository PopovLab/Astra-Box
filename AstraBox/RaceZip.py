import encodings
import json
from zipfile import ZipFile
import zipfile

from returns.pipeline import is_successful
from returns.result import Failure

from AstraBox import Astra
from AstraBox.Models import ModelFactory
from AstraBox.WorkSpace import WorkSpace
from AstraBox.Task import Task


def create_race_zip(work_space: WorkSpace, task: Task):
    print('create_race_zip')
    res = work_space.join_path('race_data.zip')
    if is_successful(res): 
        zip_file= res.unwrap()
        try :
            prepare_task_zip(work_space, task, zip_file)
        except Exception as e :
            res = Failure(f"{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: \n{e}")
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
            exp_model = ModelFactory.load(folder_item)
            pack_model_to_zip(zip, exp_model)
        #exp_model = get('ExpModel', task.exp)
        if exp_model is None:
            raise Exception(f"ExpModel {task.exp} not exists")

        equ_model = None
        equ_model = ModelFactory.get('EquModel', task.equ)
        pack_model_to_zip(zip, equ_model)
        if equ_model is None:
            raise Exception(f"ExpModel {task.equ} not exists")

        models  = {
            'ExpModel' : exp_model.data,
            'EquModel' : equ_model.data,
            'name' : task.name
            }
        
        if task.rt is not None: # старая версия модели v1
            rt_model =  ModelFactory.get('RTModel', task.rt)
            if rt_model:
                models['RTModel'] = rt_model.data
                pack_model_to_zip(zip, rt_model)
                pack_model_to_zip(zip, rt_model.get_spectrum_model())
                with zip.open( 'race_model.json' , "w" ) as json_file:
                    json_writer = encodings.utf_8.StreamWriter(json_file) 
                    # JSON spec literally fixes interchange encoding as UTF-8: https://datatracker.ietf.org/doc/html/rfc8259#section-8.1
                    json.dump(models, json_writer, ensure_ascii=False, indent=2)                
        elif task.frtc is not None: # новая версия v2
            frtc_model = ModelFactory.get('FRTCModel', task.frtc)
            spectrum_model = ModelFactory.get('SpectrumModel', task.spectrum)
            #zip.writestr('lhcd/ray_tracing.dat', frtc_model.export_to_text(spectrum_model.spectrum.kind, spectrum_model.spectrum.PWM))
            frtc_nml = frtc_model.export_to_nml()
            spm_nml  = spectrum_model.export_to_nml()
            zip.writestr('lhcd/parameters.nml', frtc_nml + '\n' + spm_nml)
            zip.writestr('lhcd/spectrum.dat', spectrum_model.export_to_text())
            #pack_model_to_zip(zip, frtc_model)
            #pack_model_to_zip(zip, spectrum_model)
            model_dump_to_zip(zip, model= frtc_model, file_name='frtc_model.json')
            model_dump_to_zip(zip, model= spectrum_model, file_name='spectrum_model.json')

        for key, item in work_space.folder_content('SbrModel').items():
            pack_model_to_zip(zip, ModelFactory.load(item))

