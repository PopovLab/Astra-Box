import os
import json
import pathlib 
import zipfile
import datetime
from AstraBox.Models.BaseModel import BaseModel
from AstraBox.Storage import Storage

class RaceHelper:
    def __init__(self, exp_model, equ_model, rt_model) -> None:
        self.exp_model = exp_model
        self.equ_model = equ_model
        self.rt_model = rt_model
        #self.race_model = RaceModel('race_model')



class RaceModel(BaseModel):

    def __init__(self, name = None, model= None, exp_name = None, equ_name = None, rt_name = None) -> None:
        super().__init__(name, model)
        self._setting = None
        self.changed = False
        self.exp_model = Storage().exp_store.data[exp_name]
        self.equ_model = Storage().equ_store.data[equ_name]
        self.rt_model = Storage().rt_store.data[rt_name]
        self.race_zip_file = None

    @property
    def model_name(self):
        return 'RaceModel'   

    def get_work_folder(self):
        return "data\\test_work_folder"

    def prepare_model_data(self, model):
        file_name = model.get_dest_path()        
        dest_folder = self.get_work_folder()
        dest = os.path.join(dest_folder, file_name)
        data = model.get_text()
        f = open(dest, "w")
        f.write(data)
        f.close()

    def pack_model_to_zip(self, zip, model):
        file_name = model.get_dest_path()        
        data = model.get_text()
        zip.writestr(file_name,data)
        #with zip.open(file_name, mode='w') as f:
        #    f.writestr(data)
        #    f.close

    def generate_race_name(self, prefix):
        dt_string = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        return f'{prefix}_{dt_string}.zip'

    def prepare_run_data(self):
        zip_file = 'Data/races/race_data.zip'
        with zipfile.ZipFile(zip_file, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel = 2) as zip:
            self.pack_model_to_zip(zip, self.exp_model)
            self.pack_model_to_zip(zip, self.equ_model)
            self.pack_model_to_zip(zip, self.rt_model)
            for key, item in Storage().sbr_store.data.items():
                self.pack_model_to_zip(zip, item)
        
        return zip_file