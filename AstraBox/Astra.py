from pydantic import BaseModel, Field

basic_folder = {
    'DATA'         : "dat/",
    'RADIAL_DATA'  : "dat/XData/" 
}

data_folder = {
    'DATA'         : "dat/",
    'RADIAL_DATA'  : "dat/XData/",
    'DIFFUSION'    : 'lhcd/diffusion/',
    'MAXWELL'      : 'lhcd/maxwell/',
    'MAXWELL_fij0' : 'lhcd/maxwell_fij0/',
    'DISTRIBUTION' : 'lhcd/distribution/',
    'TRAJECTROY'   : 'lhcd/traj/',
    'TRAJ_POS'     : 'lhcd/traj/pos/',
    'TRAJ_NEG'     : 'lhcd/traj/neg/',
    'POWER_POS'    : 'lhcd/lhcd_power/pos/',
    'POWER_NEG'    : 'lhcd/lhcd_power/neg/',    
    'RT_RESULT'    : 'lhcd/rt-result/',
    'DC'           : 'lhcd/driven_current/',
    'lhcd_out'     : 'lhcd/out/',
    'plasma'       : 'lhcd/plasma/',
    'lhcd'         : 'lhcd/'
}


class AstraProfile(BaseModel):
    type:str    = Field(default='WSL')
    name:str    = Field(default='Astra-6 a4')
    home:str    = Field(default='/home/linux_user/ASTRA-6')
    profile:str = Field(default='a4')
    dest:str    = Field(default='\\\\wsl$\\Ubuntu-20.04\\home\\linux_user\\ASTRA-6')

    data: list[str]


class ProfileList(BaseModel):
    profiles:list[AstraProfile]
