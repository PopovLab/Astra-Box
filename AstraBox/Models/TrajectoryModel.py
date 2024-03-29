import pathlib 
import numpy as np
from AstraBox.Models.RaceModel import RaceModel

def path_to_time(p):
    p = pathlib.Path(p)
    if p.suffix != '.dat': return 0.0
    return float(p.stem)

class TrajectoryModel:
    def __init__(self, race_model:RaceModel, folder_name: str) -> None:
        self.race_model = race_model
        self.folder_name = folder_name
        self.version = 1
        
        if self.race_model.check_v2_file(self.folder_name):
            self.version = 2 
            self.traj_cache = {}
            self.trajectory_series_list = self.race_model.get_data_files(self.folder_name)
            self.start_time, self.finish_time = self.get_interval()
            self.num_traj = len(self.trajectory_series_list)
        else:
            self.trajectory_series_list = self.race_model.get_data_files(self.folder_name)
            self.rays_cache = {}
            self.num_traj = len(self.trajectory_series_list)
            if self.num_traj>0: 
                self.rays, self.start_time  = self.get_rays(0)
                _, self.finish_time  = self.get_rays(self.num_traj-1)

    def get_interval(self):
        start = path_to_time(self.trajectory_series_list[0])
        finish = path_to_time(self.trajectory_series_list[-1])
        return start, finish

    def get_rays(self, index):
        if not index in self.rays_cache:
            print(f'{index} not in cache')
            self.rays_cache[index] = self.race_model.get_rays(self.trajectory_series_list[index])
        rays, time_stamp = self.rays_cache[index]        
        return rays, time_stamp

    def update_theta_interval(self):
        self.max_theta = max(self.traj_series, key=lambda x:x['theta'])['theta']
        self.min_theta = min(self.traj_series, key=lambda x:x['theta'])['theta']

    def update_spectrum_interval(self):
        self.max_spectrum_index = max(self.traj_series, key=lambda x:x['index'])['index']
        self.min_spectrum_index = min(self.traj_series, key=lambda x:x['index'])['index']

    def update_power_density_interval(self):
        self.max_power_density_interval = max(self.traj_series, key=lambda x:x['power_density'])['power_density']
        self.min_power_density_interval = min(self.traj_series, key=lambda x:x['power_density'])['power_density']


    def read_trajectory_series(self, fn):
        ts= self.race_model.read_trajectory_series(fn)
        for series in ts:
            if not series['traj'] is None:
                traj = series['traj']
                traj['length'] = np.sqrt(np.square(traj['R'].diff()) + np.square(traj['Z'].diff()))
                #traj['length'][0] = 1.0
                traj['delta_power'] = traj['P_tot'].diff()
                traj['power_density'] = traj['delta_power']/traj['length']
                #print(traj.head)
        return ts

    def select_series(self, index):
        self.time_stamp = path_to_time(self.trajectory_series_list[index])
        
        if not index in self.traj_cache:
            self.traj_cache[index] = self.read_trajectory_series(self.trajectory_series_list[index])
        self.traj_series = self.traj_cache[index]

    def get_term_list(self):
        for series in self.traj_series:
            if not series['traj'] is None:
                traj = series['traj']
                break
        return  ['index'] + list(traj.columns)