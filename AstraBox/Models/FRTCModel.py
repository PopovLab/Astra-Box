import pathlib 
from typing import Literal
from typing_extensions import Annotated
from typing import ClassVar
from pydantic import BaseModel, Field

#import AstraBox.WorkSpace as WorkSpace


class Text(BaseModel):
    title: str
    text: list[str]

class Float(BaseModel):
    title: str
    unit: str = None
    value: float
    description: str

class ParametersSection(BaseModel):
    title: str

class ctype(BaseModel):
    kind: str

class PhysicalParameters(ParametersSection):
    title: ClassVar[str] = 'Physical Parameters'
    freq: float = Field(default= 5.0, title= 'Frequency', unit= 'GHz', description= "RF frequency, GHz")
    xmi1: float = Field(default= 2.0, title= 'xmi1', description= "Mi1/Mp,  relative mass of ions 1")
    zi1:  float = Field(default= 1.0, title= 'zi1',  description= "charge of ions 1")
    xmi2: float = Field(default= 16.0,title= 'xmi2', description= "Mi2/Mp,  relative mass of ions 2")
    zi2:  float = Field(default= 0.0, title= 'zi2',  description= "charge of ions 2")
    dni2: float = Field(default= 0.03,title= 'dni2', description= "Ni2/Ni1, relative density of ions 2")
    xmi3: float = Field(default= 1.0, title= 'xmi3', description= "Mi3/Mp,  relative mass of ions 3")
    zi3:  float = Field(default= 1.0, title= 'zi3',  description= "charge of ions 3")
    dni3: float = Field(default= 1.0, title= 'dni3', description= "Ni3/Ni1, relative density of ions 3")

class AlphasParameters(ParametersSection):
    title: ClassVar[str] = 'Parameters for alphas calculations'
    itend0: int   = Field(default= 0,    title= 'itend0', description= "if = 0, no alphas")
    energy: float = Field(default= 30.0, title= 'energy', description= "max. perp. energy of alphas (MeV", unit= 'MeV')
    factor: float = Field(default= 10.0, title= 'factor', description= "factor in alpha source")
    dra:    float = Field(default= 0.3,  title= 'dra',    description= "relative alpha source broadening (dr/a)")
    kv: int       = Field(default= 30,  title= 'kv',      description= "V_perp  greed number")

class NumericalParameters(ParametersSection):
    title: ClassVar[str] = 'Numerical parameters'
    nr:     int = Field(default= 30, title= 'nr',    description= "radial grid number  <= 505")

    hmin1:  float = Field(default= 1.e-6, title= 'hmin1',  description= "rel.(hr) min. step in the Fast comp. mode, <1.d0")   
    rrange: float = Field(default= 1.e-4, title= 'rrange', description= "rel.(hr) size of a 'turning' point region, <1.d0")    
    eps:    float = Field(default= 1.e-6, title= 'eps',    description= "accuracy")          
    hdrob:  float = Field(default= 1.5,   title= 'hdrob',  description= "h4 correction")
    cleft:  float = Field(default= 0.7,   title= 'cleft',  description= "left Vz plato border shift (<1)")
    cright: float = Field(default= 1.5,   title= 'cright', description= "right Vz plato border shift (>1)")
    cdel:   float = Field(default= 0.25,  title= 'cdel',   description= "(left part)/(Vz plato size)")
    rbord:  float = Field(default= 0.999, title= 'rbord',  description= "(relative radius of reflection, <1.")
    pchm:   float = Field(default= 0.2,   title= 'pchm',   description= "threshold between 'strong' and weak' absorption, <1.")
    pabs:   float = Field(default= 1.e-2, title= 'pabs',   description= "part of remaining power interp. as absorption")
    pgiter: float = Field(default= 1.e-4, title= 'pgiter', description= "relative accuracy to stop iterations")

    ni1:     int = Field(default= 20, title= 'ni1',    description= "grid number in the left part of Vz plato")
    ni2:     int = Field(default= 20, title= 'ni2',    description= "grid number in the right part of Vz plato")

    niterat: int = Field(default= 99, title= 'niterat',    description= "maximal number of iterations")
    nmaxm_1: int = Field(default= 20, title= 'nmaxm(1)',    description= "permitted reflections at 0 iteration")
    nmaxm_2: int = Field(default= 20, title= 'nmaxm(2)',    description= "permitted reflections at 2 iteration")
    nmaxm_3: int = Field(default= 20, title= 'nmaxm(3)',    description= "permitted reflections at 3 iteration")
    nmaxm_4: int = Field(default= 20, title= 'nmaxm(4)',    description= "permitted reflections at 4 iteration")
    maxstep2:int = Field(default= 1000, title= 'maxstep2',    description= "maximal steps' number in Fast comp. mode")
    maxstep4:int = Field(default= 1000, title= 'maxstep4',    description= "maximal steps' number in Slow comp. mode")
 

class Options(ParametersSection):
    title: ClassVar[str] = 'Options'

    ipri:     int = Field(default= 2, title= 'ipri',    description= "printing output monitoring: 0,1,2,3,4")
    iw:       int = Field(default= 1, title= 'iw',      description= "initial mode (slow=1, fast=-1)")
    ismth:    int = Field(default= 1, title= 'ismth',   description= "if=0, no smoothing in Ne(rho),Te(rho),Ti(rho)")
    ismthalf: int = Field(default= 0, title= 'ismthalf',description= "if=0, no smoothing in D_alpha(vperp)")                     
    ismthout: int = Field(default= 1, title= 'ismthout',description= "if=0, no smoothing in output profiles")
    inew: int = Field(default= 0, title= 'inew', description= "inew=0 for usual tokamak&Ntor_grill; 1 or 2 for g' in ST&Npol_grill")                   
    itor: int = Field(default= 1, title= 'itor', description= "+-1, Btor direction in right coord{drho,dteta,dfi}")    
    ipol: int = Field(default= 1, title= 'ipol', description= "+-1, Bpol direction in right coord{drho,dteta,dfi}")    


class GrillParameters(ParametersSection):
    title: ClassVar[str] = 'Grill parameters'

    Zplus: float = Field(default= 11, title='Zplus', description='upper grill corner in centimeters', unit='cm')
    Zminus: float = Field(default= -11, title='Zminus', description='lower grill corner in centimeters', unit='cm')

    ntet: int = Field(default= 21, title='ntet', description='theta grid number')
    nnz:  int = Field(default= 51, title='nnz', description='iN_phi grid numbe')




class FRTCModel(BaseModel):
    name:  str = Field(default= '123', title='name')
    comment: str = Field(default='ccc', title='Comment')

    physical_parameters: PhysicalParameters = Field(default= PhysicalParameters())

    alphas_parameters: AlphasParameters = Field(default= AlphasParameters())

    numerical_parameters: NumericalParameters = Field(default= NumericalParameters())

    options: Options = Field(default= Options())

    grill_parameters: GrillParameters = Field(default= GrillParameters())

    def get_sections(self):
        return [
            self.physical_parameters,
            self.alphas_parameters,
            self.numerical_parameters,
            self.options,
            self.grill_parameters
            ]


def save_rtp(rtp, fn):
    loc = pathlib.Path(fn)
    with open(loc, "w" ) as file:
            file.write(rtp.model_dump_json(indent= 2))

if __name__ == '__main__':
    frtc = FRTCModel()
    save_rtp(frtc, 'test_frtc_model.txt')
    for sec in frtc.get_sections():
        print('-----------------------------')
        print(sec)
        schema= sec.model_json_schema()['properties']
        print(schema)
        for name, value in sec:
            s = schema[name]
            print(f' - {s["title"]}: {value}  -- {s.get("description")}')
            print(s)
