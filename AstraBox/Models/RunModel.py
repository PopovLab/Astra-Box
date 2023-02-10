import os
import json
import encodings
import pathlib 
import zipfile
import datetime
from AstraBox.Models.BaseModel import BaseModel
import AstraBox.Models.ModelFactory as ModelFactory
import AstraBox.WorkSpace as WorkSpace

def float_try(str):
    try:
        return float(str)
    except ValueError:
        return 0.0

class RunModel(BaseModel):

    def __init__(self, name = None, exp_name = None, equ_name = None, rt_name = None) -> None:
        super().__init__(name)
        self._setting = None
        self.changed = False
        self.exp_model = ModelFactory.build(WorkSpace.getDataSource('exp').items[exp_name])
        self.equ_model = ModelFactory.build(WorkSpace.getDataSource('equ').items[equ_name])
        self.rt_model = ModelFactory.build(WorkSpace.getDataSource('ray_tracing').items[rt_name])            
 
        self.data['ExpModel'] = self.exp_model.data
        self.data['EquModel'] = self.equ_model.data
        self.data['RTModel'] = self.rt_model.data
        self.race_zip_file = None

    @property
    def model_name(self):
        return 'RunModel'   

    def get_work_folder(self):
        return "data\\races"

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

    def load_model_data(self):
        with zipfile.ZipFile(self.race_zip_file) as zip:
            with zip.open( 'race_model.json' , "r" ) as json_file:
                self.data = json.load(json_file)

    def get_models_dict(self):
        return {
            'RaceModel' : self.data,
            "exp_model" : self.exp_model.data,
            "equ_model" : self.equ_model.data,
            "rt_model" : self.rt_model.data,
        }

    def prepare_run_data(self):
        zip_file = os.path.join(str(WorkSpace.getInstance().destpath), 'race_data.zip')
        with zipfile.ZipFile(zip_file, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel = 2) as zip:
            self.pack_model_to_zip(zip, self.exp_model)
            self.pack_model_to_zip(zip, self.equ_model)
            self.pack_model_to_zip(zip, self.rt_model)
            self.pack_model_to_zip(zip, self.rt_model.get_spectrum_model())
            for key, item in WorkSpace.getDataSource('sbr').items.items():
                self.pack_model_to_zip(zip, ModelFactory.build(item))
            with zip.open( 'race_model.json' , "w" ) as json_file:
                json_writer = encodings.utf_8.StreamWriter(json_file)
                # JSON spec literally fixes interchange encoding as UTF-8: https://datatracker.ietf.org/doc/html/rfc8259#section-8.1
                json.dump(self.data, json_writer, ensure_ascii=False, indent=2)
        return zip_file