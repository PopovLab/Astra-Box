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