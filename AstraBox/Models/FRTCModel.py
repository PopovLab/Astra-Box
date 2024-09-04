import pathlib 
from typing import Literal
from typing_extensions import Annotated
from typing import ClassVar
from pydantic import BaseModel, Field

#import AstraBox.WorkSpace as WorkSpace

class String(BaseModel):
    title: str
    text: str

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
    freq: float = Field(title= 'Frequency', default=5.0, unit= 'GHz', description= "RF frequency, GHz")
    xmi1: float = Field(title= 'xmi1', default= 2.0, description= "Mi1/Mp,  relative mass of ions 1")
    zi1:  float = Field(title= 'zi1', default= 1.0, description= "charge of ions 1")
    xmi2: float = Field(title= 'xmi2', default= 16.0,  description= "Mi2/Mp,  relative mass of ions 2")
    zi2:  float = Field(title= 'zi2', default= 0.0,  description= "charge of ions 2")
    dni2: float = Field(title= 'dni2', default= 0.03, description= "Ni2/Ni1, relative density of ions 2")
    xmi3: float = Field(title= 'xmi3', default= 1.0, description= "Mi3/Mp,  relative mass of ions 3")
    zi3:  float = Field(default= 1.0, title= 'zi3',  description= "charge of ions 3")
    dni3: float = Field(default= 1.0, title= 'dni3', description= "Ni3/Ni1, relative density of ions 3")

class AlphasParameters(ParametersSection):
    title: ClassVar[str] = 'Parameters for alphas calculations'

class NumericalParameters(ParametersSection):
    title: ClassVar[str] = 'Numerical parameters'



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
    name:  String = Field(default= String(title='name', text= ''))

    comments: Text = Field(default= Text(title='Comments', text= []))

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
    #loc = WorkSpace.get_location_path().joinpath(fn)

    loc = pathlib.Path(fn)
    with open(loc, "w" ) as file:
            file.write(rtp.model_dump_json(indent= 2))

if __name__ == '__main__':
    frtc = FRTCModel()
    save_rtp(frtc, 'test_frtc_model.txt')

    o = frtc.options

    print(o.xyz)
    o.zyx = 31.415
    print(o.zyx)
    #print(pp.zyx.title)
    #print(o.model_json_schema())
    for sec in frtc.get_sections():
        print('-----------------------------')
        print(sec)
        schema= sec.model_json_schema()['properties']
        print(schema)
        for name, value in sec:
            s = schema[name]
            print(f' - {s["title"]}: {value}  -- {s.get("description")}')
            print(s)

