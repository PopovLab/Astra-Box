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
from AstraBox.Models.Spectrum import GaussSpectrum, ScatterSpectrum, Spectrum1D



def random_name():
    return 'new_'+str(uuid.uuid4())[0:4]

class SpectrumModel(BaseModel):
    name:  str = Field(default= '123', title='name')
    comment: str = Field(default='ccc', title='Comment')
    spectrum: GaussSpectrum | Spectrum1D | ScatterSpectrum= Field(default= GaussSpectrum(kind='gauss_spectrum'))

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
            case 'scatter_spectrum':
                return cls(name= name, spectrum=ScatterSpectrum(kind='scatter_spectrum'))            
            case _:
                return cls(name= name)

    def get_dump(self):
        return self.model_dump_json(indent= 2)