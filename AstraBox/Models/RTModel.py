import os
import json
import pathlib 
from AstraBox.Models.BaseModel import BaseModel

def default_rt_setting():
        return {
            'Comments':{
                    'value' : 'Comments about ....',
                    'title' : 'Comments',
                    'type' : 'text'
                },
            'Physical parameters': {
                "Freq": { 
                    'title' : 'Frequency',
                    'value' : 5.0, 
                    'unit'  : 'GHz',
                    'type': 'float',                    
                    'description' : "RF frequency, GHz"
                },
                "xmi1": { 
                    'title' : 'xmi1',
                    'value' : 2.0, 
                    'type': 'float',
                    'description' : "Mi1/Mp,  relative mass of ions 1"
                },                
               "zi1": { 
                    'title' : 'zi1',
                    'value' : 1.0, 
                    'type': 'float',
                    'description' : "charge of ions 1"
                },                
               "xmi2": { 
                    'title' : 'xmi2',
                    'value' : 16.0, 
                    'type': 'float',
                    'description' : "Mi2/Mp,  relative mass of ions 2"
                },                        
               "zi2": { 
                    'title' : 'zi2',
                    'value' : 0.0, 
                    'type': 'float',
                    'description' : "charge of ions 2"
                },
               "dni2": { 
                    'title' : 'dni2',
                    'value' : 0.03, 
                    'type': 'float',
                    'description' : "Ni2/Ni1, relative density of ions 2"
                },
               "xmi3": { 
                    'title' : 'xmi3',
                    'value' : 1.00, 
                    'type': 'float',
                    'description' : "Mi3/Mp,  relative mass of ions 3"
                },
               "zi3": { 
                    'title' : 'zi3',
                    'value' : 1.00, 
                    'type': 'float',
                    'description' : "charge of ions 3"
                },
               "dni3": { 
                    'title' : 'dni3',
                    'value' : 1.00, 
                    'type': 'float',
                    'description' : "Ni3/Ni1, relative density of ions 3"
                },
            },
            "Options" :{
                'Xwkb/Np':{
                    'value': 'Automatic',
                    'type': 'enum',
                    'value_items' : ['Manual', 'Automatic'],
                    'title' : 'Xwkb/Np',
                    'description': 'type int (0-Manual, 1-Automatic)'
                },
                "Xwkb":{
                    'value': 123.0,
                    'type': 'float',
                    'unit': 'cm',
                    'title' : 'Xwkb',
                    'description':"Xwkb <= Xwkbmax"
                },
                'Np':{
                    'value': 5,
                    'type': 'int',
                    'title' : 'Np',
                    'description':"Np<=Npmax"
                },
                'optimization level':{
                    'value': 'OptLevel 1',
                    'type': 'enum',
                    'value_items' : ['No optimization', 'OptLevel 0', 'OptLevel 1'],
                    'title' : 'Optimization Level',
                    'description': 'type int (OptLevel 0 - adjust only MPD, do not vary Xwkb, OptLevel 1 - adjust only MPD, and check Xwkb)'
                },                
            },

        }

    
class RTModel(BaseModel):

    def __init__(self, name = None, model= None) -> None:
        super().__init__(name, model)
        self.changed = False

    @property
    def model_name(self):
        return 'RTModel'   

    @property
    def setting(self):
        """Parameters of ray tracing"""
        if not 'setting' in self.data:
            self.data['setting'] = default_rt_setting()
        return self.data['setting']