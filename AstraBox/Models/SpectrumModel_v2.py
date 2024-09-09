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
from AstraBox.Models.Spectrum import GaussSpectrum, Spectrum1D



def random_name():
    return 'new_'+str(uuid.uuid4())[0:4]

class SpectrumModel(BaseModel):
    name:  str = Field(default= '123', title='name')
    comment: str = Field(default='ccc', title='Comment')
    spectrum: GaussSpectrum | Spectrum1D = Field(default= GaussSpectrum())

    @classmethod
    def construct(cls, dump):
        try:
            return cls.model_validate_json(dump)
        except:
            return None
        
    @classmethod
    def construct_new(cls, name: str):
        print(name)
        return cls(name= name)

    def get_dump(self):
        return self.model_dump_json(indent= 2)