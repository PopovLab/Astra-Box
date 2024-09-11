import pathlib 
import numpy as np
from typing import Literal
from typing_extensions import Annotated
from typing import ClassVar
from pydantic import BaseModel, Field


class BaseSpectrum(BaseModel):
    kind: None

class GaussSpectrum(BaseSpectrum):
    kind: Literal['gauss_spectrum']
    title: ClassVar[str] = 'Gauss Spectrum'
    x_min: float = Field(default= -40.0, title= 'x_min')
    x_max: float = Field(default= 40.0, title= 'x_max')
    step:  float = Field(default= 0.5, title= 'step')
    bias:  float = Field(default= 0.0, title= 'bias')
    sigma: float = Field(default= 2.5, title= 'sigma')
    angle: float = Field(default= 0.0, title= 'angle', unit= 'deg', description= "Rotation on spectrum")
    PWM:   bool  = Field(default= True, title= 'PWM', description= "pulse-width modulation")
    
    def make_spectrum_data(self):
      
        num = int((self.x_max - self.x_min)/self.step)
        x = np.linspace(self.x_min, self.x_max, num = num)
        bias = self.bias
        sigma = self.sigma
        y = np.exp(-0.5*((x-bias)/sigma)**2) # + np.exp(-25*((x+bias)/bias)**2)
        spectrum_data = { 'Ntor': x.tolist(), 'Amp': y.tolist()  }     
        return spectrum_data   
        #self.spectrum_normalization()
    
class Spectrum1D(BaseSpectrum):
    kind: Literal['spectrum_1D']
    title: ClassVar[str] = 'Spectrum 1D'    
    source: str   = Field(default= '', title= 'source')
    angle:  float = Field(default= 0.0, title= 'angle', unit= 'deg', description= "Rotation on spectrum")
    PWM:    bool  = Field(default= True, title= 'PWM', description= "pulse-width modulation")    


class ScatterSpectrum(BaseSpectrum):
    kind: Literal['scatter_spectrum']
    title: ClassVar[str] = 'Scatter Spectrum'    
    source: str   = Field(default= 0.0, title= 'source')
    angle:  float = Field(default= 0.0, title= 'angle', unit= 'deg', description= "Rotation on spectrum")
    PWM:    bool  = Field(default= True, title= 'PWM', description= "pulse-width modulation")  