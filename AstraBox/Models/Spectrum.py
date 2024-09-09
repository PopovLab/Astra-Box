import pathlib 
from typing import Literal
from typing_extensions import Annotated
from typing import ClassVar
from pydantic import BaseModel, Field


class BaseSpectrum(BaseModel):
    title: str

class GaussSpectrum(BaseModel):
    title: ClassVar[str] = 'Gauss Spectrum'
    x_min: float = Field(default= -40.0, title= 'x_min')
    x_max: float = Field(default= 40.0, title= 'x_max')
    step:  float = Field(default= 0.5, title= 'step')
    bias: float = Field(default= 0.0, title= 'bias')
    sigma:  float = Field(default= 2.5, title= 'sigma')
    angle:  float = Field(default= 0.0, title= 'angle', unit= 'deg', description= "Rotation on spectrum")
    PWM:  bool = Field(default= True, title= 'PWM', description= "pulse-width modulation")
    
    
class Spectrum1D(BaseModel):
    title: ClassVar[str] = 'Spectrum 1D'    
    source: str = Field(default= 0.0, title= 'source')
    angle:  float = Field(default= 0.0, title= 'angle', unit= 'deg', description= "Rotation on spectrum")
    PWM:  bool = Field(default= True, title= 'PWM', description= "pulse-width modulation")    
