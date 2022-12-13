import os
import json
import encodings
import pathlib 
import zipfile
import datetime
from AstraBox.Models.BaseModel import BaseModel
import AstraBox.Models.RadialData as RadialData
import AstraBox.Models.Distribution as Distribution
import AstraBox.Models.ModelFactory as ModelFactory
import AstraBox.WorkSpace as WorkSpace
import AstraBox.Models.DataSeries as DataSeries


class RaceHelper:
    def __init__(self, exp_model, equ_model, rt_model) -> None:
        self.exp_model = exp_model
        self.equ_model = equ_model
        self.rt_model = rt_model
        #self.race_model = RaceModel('race_model')

def float_try(str):
    try:
        return float(str)
    except ValueError:
        return 0.0

class RaceModel(BaseModel):

    def __init__(self, name = None, exp_name = None, equ_name = None, rt_name = None, path = None) -> None:
        super().__init__(name)
        if path:
            self._path = path
            self.race_zip_file = str(path)
            print(self.race_zip_file)
            self.name = path.name
        else:
            self._setting = None
            self.changed = False
            self.exp_model = ModelFactory.build(WorkSpace.getDataSource('exp').items[exp_name])
            self.equ_model = ModelFactory.build(WorkSpace.getDataSource('equ').items[equ_name])
            self.rt_model = ModelFactory.build(WorkSpace.getDataSource('ray_tracing').items[rt_name])            
            #self.exp_model = Storage().exp_store.data[exp_name]
            #self.equ_model = Storage().equ_store.data[equ_name]
            #self.rt_model = Storage().rt_store.data[rt_name]
            self.data['ExpModel'] = self.exp_model.data
            self.data['EquModel'] = self.equ_model.data
            self.data['RTModel'] = self.rt_model.data
            self.race_zip_file = None

    @property
    def model_name(self):
        return 'RaceModel'   

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
            for key, item in WorkSpace.getDataSource('sbr').items.items():
                self.pack_model_to_zip(zip, ModelFactory.build(item))
            with zip.open( 'race_model.json' , "w" ) as json_file:
                json_writer = encodings.utf_8.StreamWriter(json_file)
                # JSON spec literally fixes interchange encoding as UTF-8: https://datatracker.ietf.org/doc/html/rfc8259#section-8.1
                json.dump(self.data, json_writer, ensure_ascii=False, indent=2)
        return zip_file


    def get_radial_data_list(self):
        return self.get_file_list('dat/')

    def read_radial_data(self,f):
        with zipfile.ZipFile(self.race_zip_file) as zip:
            with zip.open(f) as file:
                return RadialData.read_radial_data(file)        

    def get_file_list(self, folder):
        length = len(folder)
        with zipfile.ZipFile(self.race_zip_file) as zip:
            list =  [ z.filename for z in zip.filelist if (z.filename.startswith(folder)  and len(z.filename)>length )]
        list.sort()  
        return list

    def get_diffusion_list(self):
        return self.get_file_list('lhcd/diffusion/')   

    def read_diffusion(self, f):
        p = pathlib.Path(f)
        print(p.suffix)
        print(p.stem)
        if p.suffix != '.dat': return
        time_stamp = float(p.stem)
        with zipfile.ZipFile(self.race_zip_file) as zip:
            with zip.open(f) as file:
                return DataSeries.get_maxwell(file), time_stamp      

    def get_maxwell_distr_list(self):
        return self.get_file_list('lhcd/maxwell/')    

    def read_maxwell_distribution(self, f):
        p = pathlib.Path(f)
        print(p.suffix)
        print(p.stem)
        if p.suffix != '.dat': return
        time_stamp = float(p.stem)
        with zipfile.ZipFile(self.race_zip_file) as zip:
            with zip.open(f) as file:
                return DataSeries.get_maxwell(file), time_stamp        

    def get_distribution_list(self):
        return self.get_file_list('lhcd/distribution/')             

    def read_distribution(self, f):
        p = pathlib.Path(f)
        print(p.suffix)
        print(p.stem)
        if p.suffix != '.dat': return
        try:
            time_stamp = float(p.stem)
        except ValueError:
            return [], 0.0
        with zipfile.ZipFile(self.race_zip_file) as zip:
            with zip.open(f) as file:
                return Distribution.get(file), time_stamp

    def get_trajectory_list(self):
        tmp = 'lhcd/out/traj'
        with zipfile.ZipFile(self.race_zip_file) as zip:
            list =  [ z.filename for z in zip.filelist if (z.filename.startswith(tmp))]
        list.sort()  
        return list            

    def get_rays(self, f):
        time_stamp = float(f[13:20])
        print(time_stamp)
        with zipfile.ZipFile(self.race_zip_file) as zip:
            with zip.open(f) as file:
                header = file.readline().decode("utf-8").replace('=', '_').split()

                lines = file.readlines()
                table = [line.decode("utf-8").split() for line in lines]
                table = list(filter(None, table))

                rays = []
                N_traj = 0

                for row in table:
                    if N_traj != int(row[12]):
                        N_traj = int(row[12])
                        ray = dict([ (h, []) for h in header ])
                        rays.append(ray)
                    for index, (p, item) in enumerate(ray.items()):
                        item.append(float_try(row[index]))
        return rays, time_stamp        


    def read_plasma_bound(self):
        Icms_path = 'lhcd/out/lcms.dat'
        with zipfile.ZipFile(self.race_zip_file) as zip:
            with zip.open(Icms_path) as file:
                header = file.readline().split()
                #print(header)
                lines = file.readlines()

                table = [line.split() for line in lines]
                table = list(filter(None, table))

                R = [float(row[0]) for row in table]
                Z = [float(row[1]) for row in table]
        return R, Z