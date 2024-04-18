import pathlib 
from typing import Literal
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

class PhysicalParameters(ParametersSection):
    title: str = 'Physical Parameters'
    xyz:  float = Field(default= 1.23, title='test xyz', description='xyz test')
    freq: Float = Field(default= Float(title= 'Frequency', value=5.0, unit= 'GHz', description= "RF frequency, GHz"))
    xmi1: Float = Field(default= Float(title= 'xmi1', value= 2.0, description= "Mi1/Mp,  relative mass of ions 1"))
    zi1:  Float = Field(default= Float(title= 'zi1', value= 1.0, description= "charge of ions 1"))
    xmi2: Float = Field(default= Float(title= 'xmi2', value= 16.0,  description= "Mi2/Mp,  relative mass of ions 2"))
    zi2:  Float = Field(default= Float(title= 'zi2', value= 0.0,  description= "charge of ions 2"))
    dni2: Float = Field(default= Float(title= 'dni2', value= 0.03, description= "Ni2/Ni1, relative density of ions 2"))
    xmi3: Float = Field(default= Float(title= 'xmi3', value= 1.0, description= "Mi3/Mp,  relative mass of ions 3"))
    zi3:  Float = Field(default= Float(title= 'zi3', value= 1.0, description= "charge of ions 3"))
    dni3: Float = Field(default= Float(title= 'dni3', value= 1.0, description= "Ni3/Ni1, relative density of ions 3"))

class AlphasParameters(ParametersSection):
    title: str = 'Parameters for alphas calculations'

class NumericalParameters(ParametersSection):
    title: str = 'Numerical parameters'

class Options(ParametersSection):
    title: str = 'Options'

class GrillParameters(ParametersSection):
    title: str = 'Grill parameters'


class RTParameters(BaseModel):
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


def test_rtp(rtp, fn):
    #loc = WorkSpace.get_location_path().joinpath(fn)

    loc = pathlib.Path(fn)
    with open(loc, "w" ) as file:
            file.write(rtp.model_dump_json(indent= 2))

if __name__ == '__main__':
    rtp = RTParameters()
    for sec in rtp.get_sections():
        print(sec)
        for name, value in sec:
            print(f'{name}: {value}')

    test_rtp(rtp, 'test_rtp.txt')