import os
import pathlib 
import numpy as np
from typing import Literal
from typing_extensions import Annotated
from typing import ClassVar
from pydantic import BaseModel, Field

import AstraBox.WorkSpace as WorkSpace


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
    

def load_spcp1D(p: pathlib.Path):        
    if p:
        with p.open() as file:
            header = ['Ntor', 'Amp']
            print(header)
            spectrum = { h: [] for h in header }
            lines = file.readlines()
            table = []
            for line in lines:
                table.append(line.split())
            for row in table:
                for index, (p, item) in enumerate(spectrum.items()):
                    item.append(float(row[index]))
            spectrum_data = spectrum 
    else:
        spectrum_data = { 'Ntor': [], 'Amp': []  }
    return spectrum_data
    
class Spectrum1D(BaseSpectrum):
    kind: Literal['spectrum_1D']
    title: ClassVar[str] = 'Spectrum 1D'    
    source: str   = Field(default= '', title= 'source')
    angle:  float = Field(default= 0.0, title= 'angle', unit= 'deg', description= "Rotation on spectrum")
    PWM:    bool  = Field(default= True, title= 'PWM', description= "pulse-width modulation")    

    def read_spcp1D(self):        
        p = WorkSpace.get_spectrum_dat_file_path(self.source)
        spectrum_data = load_spcp1D(p)
        #self.spectrum_normalization()     
        return spectrum_data


class ScatterSpectrum(BaseSpectrum):
    kind: Literal['scatter_spectrum']
    title: ClassVar[str] = 'Scatter Spectrum'    
    source: str   = Field(default= '', title= 'source')
    angle:  float = Field(default= 0.0, title= 'angle', unit= 'deg', description= "Rotation on spectrum")
    PWM:    bool  = Field(default= True, title= 'PWM', description= "pulse-width modulation")  

    def read_scatter(self):
        p = WorkSpace.get_spectrum_dat_file_path(self.source)
        print(p)
        try:
            with p.open() as file:
                return self.read_data(file)
        except:
            print(f"Couldn't open {p}")
            return None


    def read_data(self, file):
        print('read_data')
        data = { 'Ntor': [], 'Npol': [], 'Amp':[]}
        lines = file.readlines()
        table = []
        for line in lines:
            #if isBlank(line): break
            #print(line)
            if type(line) is str:
                table.append(line.split())    
            else:                
                table.append(line.decode("utf-8").split())
        #print(len(table))
        for row in table:
            for index, (p, item) in enumerate(data.items()):
                #print(p, item, index)
                try:
                    item.append(float(row[index]))
                except ValueError:
                    item.append(0.0)
        return data