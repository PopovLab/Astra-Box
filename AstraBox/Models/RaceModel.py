import os
import json
import encodings
import pathlib 
import zipfile
import numpy as np
import pandas as pd
from io import BytesIO
from AstraBox.Models.BaseModel import BaseModel
import AstraBox.Models.RadialData as RadialData
import AstraBox.Models.DataSeries as DataSeries
from AstraBox.Models.SpectrumModel import SpectrumModel
import AstraBox.Astra as Astra

def float_try(str):
    try:
        return float(str)
    except ValueError:
        return 0.0

class RaceModel(BaseModel):

    def __init__(self, path = None) -> None:
        super().__init__('default_name')
        self._path = path
        self.race_zip_file = str(path)
        print(self.race_zip_file)
        self.name = path.name


    @property
    def model_kind(self):
        return 'RaceModel'   

    def load_model_data(self):
        try:
            with zipfile.ZipFile(self.race_zip_file) as zip:
                with zip.open( 'race_model.json' , "r" ) as json_file:
                    self.data |= json.load(json_file)
        except:
            print('error')

    def get_models_dict(self):
        return {
            'RaceModel' : self.data,
            "exp_model" : self.exp_model.data,
            "equ_model" : self.equ_model.data,
            "rt_model" : self.rt_model.data,
        }


    def read_exec_time(self, f):
        try:
            with zipfile.ZipFile(self.race_zip_file) as zip:
                with zip.open(f) as file:
                    return pd.read_csv(file, delim_whitespace=True, names=['X', 'Y'])     
        except Exception as error:
            print(error)
            return { 'X' : [], 'Y': [] }
        
    def get_exec_time(self):
        series = {}
        series['lhcd'] = self.read_exec_time('lhcd/lhcd_time.dat')
        series['driven current'] = self.read_exec_time('lhcd/drivencurrent_time.dat')
        return series

    def read_dat(self, fn) -> pd.DataFrame:
        try:
            with zipfile.ZipFile(self.race_zip_file) as zip:
                with zip.open(fn) as file:
                    return pd.read_csv(file, delim_whitespace=True)           
        except Exception as error:
            print(error)
            #return f'не смог прочитать {f}'
            return None


    def read_dat_no_header(self, fn) -> pd.DataFrame:
        try:
            with zipfile.ZipFile(self.race_zip_file) as zip:
                with zip.open(fn) as file:
                    return pd.read_csv(file, delim_whitespace=True, header=None)           
        except Exception as error:
            print(error)
            #return f'не смог прочитать {f}'
            return None

    def get_driven_current(self):
        f = 'lhcd/dc_result.dat'
        try:
            with zipfile.ZipFile(self.race_zip_file) as zip:
                with zip.open(f) as file:
                    return pd.read_csv(file, delim_whitespace=True)           
        except Exception as error:
            print(error)
            return f'не смог прочитать {f}'

    def get_time_series(self):
        f = 'dat/time_series.dat'
        try:
            with zipfile.ZipFile(self.race_zip_file) as zip:
                with zip.open(f) as file:
                    return pd.read_csv(file, delim_whitespace=True)     
        except Exception as error:
            print(error)
            return f'не смог прочитать {f}'
     

    def get_spectrum(self):
        spectrum_model = SpectrumModel(self.data['RTModel']['setting'])
        f = spectrum_model.get_dest_path()
        try:
            with zipfile.ZipFile(self.race_zip_file) as zip:
                with zip.open(f) as file:
                    spectrum_model.read_data(file)       
        except Exception as error:
            print(error)
            spectrum_model.spectrum_data = 'не смог прочитать спектр'
        return spectrum_model

    def read_radial_data(self,f):
        with zipfile.ZipFile(self.race_zip_file) as zip:
            with zip.open(f) as file:
                return RadialData.read_radial_data(file)        

    def data_files_exists(self, folder_name):
        list= self.get_data_files(folder_name)
        return True if len(list)>0 else False

    def check_v2_file(self, folder_name):
        folder = Astra.data_folder[folder_name]
        with zipfile.ZipFile(self.race_zip_file) as zip:
            p = zipfile.Path(zip, folder + 'v2')
            return p.exists()

    def get_data_files(self, folder_name):
        folder = Astra.data_folder[folder_name]
        with zipfile.ZipFile(self.race_zip_file) as zip:
            p = zipfile.Path(zip, folder)
            list = [folder + x.name for x in p.iterdir() if x.is_file() and x.suffix == '.dat']
            list.sort()  
        return list
    
    def read_maxwell_data(self, folder_name):
        p = pathlib.Path(Astra.data_folder[folder_name])
        print(p.suffix)
        print(p.stem)
        if p.suffix != '.bin': return

    def get_file_list(self, folder_name):
        folder = Astra.data_folder[folder_name]
        length = len(folder)
        with zipfile.ZipFile(self.race_zip_file) as zip:
            list =  [ z.filename for z in zip.filelist if (z.filename.startswith(folder)  and len(z.filename)>length+1 )]
            list.sort()       
        return list

    def read_diffusion(self, f):
        p = pathlib.Path(f)
        print(p.suffix)
        print(p.stem)
        if p.suffix != '.dat': return
        time_stamp = float(p.stem)
        with zipfile.ZipFile(self.race_zip_file) as zip:
            with zip.open(f) as file:
                return DataSeries.read_XY_series(file), time_stamp      

    def read_maxwell_distribution(self, f):
        p = pathlib.Path(f)
        print(p.suffix)
        print(p.stem)
        if p.suffix != '.dat': return
        time_stamp = float(p.stem)
        with zipfile.ZipFile(self.race_zip_file) as zip:
            with zip.open(f) as file:
                return DataSeries.read_XY_series(file), time_stamp        
    

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
                return DataSeries.read_original_distribution_file(file), time_stamp


    def get_rt_result(self, f):
        p = pathlib.Path(f)
        #print(p.suffix)
        #print(p.stem)
        if p.suffix != '.dat': return
        time_stamp = float(p.stem)
        #print(time_stamp)
        rt_result = { -1: {}, 1: {}}

        with zipfile.ZipFile(self.race_zip_file) as zf:
            with zf.open(f) as file:
                header = file.readline().decode("utf-8").split()
                lines = file.readlines()
                table = [line.decode("utf-8").split() for line in lines]
                table = list(filter(None, table))
                
                for row in table:
                    if row[0] == 'iteration' : continue
                    values = {}
                    for key, v in zip(header,row):
                        values[key] = float_try(v)
                    iteration = int(row[0])
                    direction = int(row[1])
                    rt_result[direction][iteration] = values
        return time_stamp, rt_result, header

    def read_trajectory_series(self, fn):
        p = pathlib.Path(fn)
        if p.suffix != '.dat': return
        time_stamp = float(p.stem)
        print(time_stamp)     
        traj_series = []
        with zipfile.ZipFile(self.race_zip_file) as zip:
            with zip.open(fn) as file:
                buffer = bytearray()
                series = None
                for item in file:
                    buffer += item
                    if len(item)<3:
                        if series is None:
                            #print(buffer)
                            series = {}
                            di= pd.read_csv(BytesIO(buffer), delim_whitespace=True).to_dict(orient='index')
                            series = di[0]
                            #print(series['info'])
                            series['traj'] = None
                            if series['mbad'] == 1:
                                traj_series.append(series)
                                series = None
                            buffer = bytearray()
                        else:
                            series['traj'] = pd.read_csv(BytesIO(buffer), delim_whitespace=True)
                            traj_series.append(series)
                            series = None
                            buffer = bytearray()
        print(len(traj_series))
        return traj_series

    def get_rays(self, f):
        ''' читаю лучи из файла и собираю их в список'''
        p = pathlib.Path(f)
        if p.suffix != '.dat': return
        time_stamp = float(p.stem)
        #time_stamp = float(f[13:20])
        print(time_stamp)
        with zipfile.ZipFile(self.race_zip_file) as zip:
            with zip.open(f) as file:
                traj = pd.read_csv(file, delim_whitespace=True)
                n_traj_list = np.unique(traj['N_traj'])
                rays = []
                for nt in n_traj_list:
                    ray = traj[traj['N_traj'] == nt]
                    rays.append(ray.reset_index(drop=True))
                    #rays.append(ray)
        return rays, time_stamp  


    def read_plasma_bound(self):
        Icms_path = 'lhcd/out/lcms.dat'
        with zipfile.ZipFile(self.race_zip_file) as zip:
            with zip.open(Icms_path) as file:
                lcms = pd.read_csv(file, delim_whitespace=True)
        return lcms.rename(columns={"R(m)": "R", "Z(m)": "Z"})

