import os
import json
import encodings
import pathlib 
import zipfile
from zipfile import ZipFile
import datetime
from AstraBox.Models.RootModel import RootModel
import AstraBox.Models.ModelFactory as ModelFactory
import AstraBox.WorkSpace as WorkSpace
import AstraBox.Astra as Astra

class RunModel(RootModel):

    def __init__(self, name:str = None, comment:str= None, exp_name = None, equ_name = None, rt_name = None) -> None:
        super().__init__(name)
        self._setting = None
        self.changed = False
        self.errors = []
        self.collection = {
            "ExpModel" : exp_name,
            "EquModel" : equ_name,
            "RTModel" : rt_name,
        }
        self.exp_model = ModelFactory.get('ExpModel', exp_name)
        if self.exp_model is None:
            self.errors.append(f"ExpModel {exp_name} not exists")

        self.equ_model =  ModelFactory.get('EquModel', equ_name)
        if self.equ_model is None:
            self.errors.append(f"EquModel {equ_name} not exists")        

        self.rt_model =  ModelFactory.get('RTModel', rt_name)
        self.comment= comment
        self.race_zip_file = None

    @property
    def model_kind(self):
        return 'RunModel'   

    def get_work_folder(self):
        return "data\\races"


    def pack_model_to_zip(self, zip, model):
        if model:
            file_name = model.get_dest_path()        
            data = model.get_text()
            zip.writestr(file_name,data)

    def generate_race_name(self, prefix):
        dt_string = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        return f'{prefix}_{dt_string}.zip'

    def load_model_data(self):
        with ZipFile(self.race_zip_file) as zip:
            with zip.open( 'race_model.json' , "r" ) as json_file:
                self.data = json.load(json_file)

    def get_models_dict(self):
        return {
            'RaceModel' : self.data,
            "exp_model" : self.exp_model.data,
            "equ_model" : self.equ_model.data,
            "rt_model" : self.rt_model.data,
        }


    def make_folders(self, zip: ZipFile):
        for key, folder in Astra.data_folder.items():
            zip.mkdir(folder)

    def prepare_run_data(self):
        #zip_file = os.path.join(str(WorkSpace.get_location_path()), 'race_data.zip')
        zip_file = WorkSpace.get_location_path().joinpath('race_data.zip')
        with ZipFile(zip_file, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel = 2) as zip:
            zip.comment = bytes(self.comment,'UTF-8')
            self.make_folders(zip)
            self.pack_model_to_zip(zip, self.exp_model)
            self.pack_model_to_zip(zip, self.equ_model)
            self.pack_model_to_zip(zip, self.rt_model)
            if self.rt_model:
                self.pack_model_to_zip(zip, self.rt_model.get_spectrum_model())
            for key, item in WorkSpace.get_models_dict('SbrModel').items():
                self.pack_model_to_zip(zip, ModelFactory.load(item.path))

            models  = {
                'ExpModel' : self.exp_model.data,
                'EquModel' : self.equ_model.data,
                'name' : self.name
                }
            if self.rt_model:
                models['RTModel'] = self.rt_model.data
                
            with zip.open( 'race_model.json' , "w" ) as json_file:
                json_writer = encodings.utf_8.StreamWriter(json_file)
                # JSON spec literally fixes interchange encoding as UTF-8: https://datatracker.ietf.org/doc/html/rfc8259#section-8.1
                json.dump(models, json_writer, ensure_ascii=False, indent=2)
        return zip_file