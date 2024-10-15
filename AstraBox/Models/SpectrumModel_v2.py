import uuid
import numpy as np
import os
from math import fsum
from pathlib import Path
import pathlib 
from typing import Literal
from typing_extensions import Annotated
from typing import ClassVar
from pydantic import BaseModel, Field
import AstraBox.WorkSpace as WorkSpace
from AstraBox.Models.Spectrum import GaussSpectrum, ScatterSpectrum, Spectrum1D, Spectrum2D



def random_name():
    return 'new_'+str(uuid.uuid4())[0:4]

class SpectrumModel(BaseModel):
    name:  str = Field(default= '123', title='name')
    comment: str = Field(default='ccc', title='Comment')
    spectrum: GaussSpectrum | Spectrum1D | Spectrum2D | ScatterSpectrum= Field(default= GaussSpectrum(kind='gauss_spectrum'))

    @classmethod
    def construct(cls, dump):
        try:
            return cls.model_validate_json(dump)
        except Exception as e:
            print(f"{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: \n{e}")
            return None
        
    @classmethod
    def construct_new(cls, name: str, spectrum_type=None):
        print(name)
        match spectrum_type:
            case 'gauss':
                return cls(name= name, spectrum=GaussSpectrum(kind='gauss_spectrum'))
            case 'spectrum_1D':
                return cls(name= name, spectrum=Spectrum1D(kind='spectrum_1D'))
            case 'spectrum_2D':
                return cls(name= name, spectrum=Spectrum2D(kind='spectrum_2D'))            
            case 'scatter_spectrum':
                return cls(name= name, spectrum=ScatterSpectrum(kind='scatter_spectrum'))            
            case _:
                return cls(name= name)

    def get_dump(self):
        return self.model_dump_json(indent= 2)
    
    def get_dest_path(self):
        return 'lhcd/spectrum.dat'

    def generate(self):
        match self.spectrum.kind:
            case 'gauss_spectrum':
                self.make_gauss_data()
            case 'rotated_gaussian':
                self.make_rotated_gauss_data()                
            case 'spectrum_1D':
                self.read_spcp1D()
            case 'scatter_spectrum':
                self.read_scatter(self.setting['source'])
            case 'spectrum_2D':
                self.read_spcp2D(self.setting['source'])

    def divide_spectrum(self):
        sp = [x for x in zip(self.spectrum_data['Ntor'], self.spectrum_data['Amp'])]
        sp_pos = [ (s[0], s[1]) for s in sp if s[0]>0]
        sp_neg = [ (-s[0], s[1]) for s in sp if s[0]<0]
        sp_neg = list(reversed(sp_neg))
        return sp_pos, sp_neg

    def export_to_text(self):
        spectrum_data = self.spectrum.get_spectrum_data()
        print(self.spectrum.kind)
        match self.spectrum.kind:
            case 'gauss_spectrum'| 'spectrum_1D':
                sp = [(x,0,p) for x, p in zip(spectrum_data['Ntor'], spectrum_data['Amp'])]
            case 'rotated_gaussian':
                sp = [(x,y,p) for x, y, p  in zip(spectrum_data['Ntor'], spectrum_data['Npol'], spectrum_data['Amp'])]                                                
            case 'scatter_spectrum':
                sp = [(x,y,p) for x, y, p  in zip(spectrum_data['Ntor'], spectrum_data['Npol'], spectrum_data['Amp'])]                                
            case 'spectrum_2D':
                sp = [(x,y,p) for x, y, p  in zip(spectrum_data['Nz'], spectrum_data['Ny'], spectrum_data['Amp'])]                
        return ''.join([f'{s[0]:.5f}  {s[1]:.5f}  {s[2]}\n' for s in sp])
    
    def export_to_nml(self):
        '''"Экспорт Spectrum параметров в nml-формат'''
        #spectrum_kind, spectrum_PWM нужно что бы знать тип спектра для файла конфигурации FRTC
        lines = []
        lines.append(f"&spectrum")
        match self.spectrum.kind:
            case 'gauss_spectrum' | 'spectrum_1D':
                if self.spectrum.PWM:
                    spect_type = 0 #   0     ! spectr type 0 - 1D + spline approximation ON
                else:
                    spect_type = 1 #   1     ! spectr type 1 - 1D + spline approximation OFF
            case 'rotated_gaussian':
                spect_type = 2     #   2     ! spectr type 2 - scatter spectrum
            case 'scatter_spectrum':
                spect_type = 2     #  2     ! spectr type 2 - scatter spectrum
            case 'spectrum_2D':
                spect_type = 3    #  3     ! spectr type 3 - 2D for futureS
        lines.append(f"spectrum_type = {spect_type}" )
        lines.append(f"spectrum_PWM = {self.spectrum.PWM}" )
        lines.append(f"spectrum_kind = {self.spectrum.kind}" )
        lines.append(f"spectrum_axis = {self.spectrum.axis}" )
        lines.append("/")
        return '\n'.join(lines)  