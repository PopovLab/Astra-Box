import os
import json
from pathlib import Path
from AstraBox.Models.BaseModel import BaseModel
from AstraBox.Models.SpectrumModel import SpectrumModel

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
            'Parameters for alphas calculations':{
                "itend0": { 
                    'title' : 'itend0',
                    'value' : 0, 
                    'type': 'int',
                    'description' : "if = 0, no alphas"
                },
               "energy": { 
                    'title' : 'energy',
                    'value' : 30.0, 
                    'type': 'float',
                    'unit' : 'MeV',
                    'description' : "max. perp. energy of alphas (MeV)"
                },
               "factor": { 
                    'title' : 'factor',
                    'value' : 10.0, 
                    'type': 'float',
                    'description' : "factor in alpha source"
                },
               "dra": { 
                    'title' : 'dra',
                    'value' : 0.3, 
                    'type': 'float',
                    'description' : "relative alpha source broadening (dr/a)"
                },
                "kv": { 
                    'title' : 'kv',
                    'value' : 30, 
                    'type': 'int',
                    'description' : "V_perp  greed number"
                },
            },
            'Numerical parameters':{
                "nr": { 
                    'title' : 'nr',
                    'value' : 30, 
                    'type': 'int',
                    'description' : "radial grid number  <= 505"
                },
               "hmin1": { 
                    'title' : 'hmin1',
                    'value' : 1.e-6, 
                    'type': 'float',
                    'description' : "rel.(hr) min. step in the Fast comp. mode, <1.d0"
                },            
               "rrange": { 
                    'title' : 'rrange',
                    'value' : 1.e-4, 
                    'type': 'float',
                    'description' : "rel.(hr) size of a 'turning' point region, <1.d0"
                },            
               "eps": { 
                    'title' : 'eps',
                    'value' : 1.e-6, 
                    'type': 'float',
                    'description' : "accuracy"
                },            
               "hdrob": { 
                    'title' : 'hdrob',
                    'value' : 1.5, 
                    'type': 'float',
                    'description' : "h4 correction"
                },            
               "cleft": { 
                    'title' : 'cleft',
                    'value' : 0.7, 
                    'type': 'float',
                    'description' : "left Vz plato border shift (<1)"
                },            
               "cright": { 
                    'title' : 'cright',
                    'value' : 1.5, 
                    'type': 'float',
                    'description' : "right Vz plato border shift (>1)"
                },            
               "cdel": { 
                    'title' : 'cdel',
                    'value' : 0.25, 
                    'type': 'float',
                    'description' : "(left part)/(Vz plato size)"
                },            
               "rbord": { 
                    'title' : 'rbord',
                    'value' : 0.999, 
                    'type': 'float',
                    'description' : "(relative radius of reflection, <1."
                },            
               "pchm": { 
                    'title' : 'pchm',
                    'value' : 0.2, 
                    'type': 'float',
                    'description' : "threshold between 'strong' and weak' absorption, <1."
                },
               "pabs": { 
                    'title' : 'pabs',
                    'value' : 1.e-2, 
                    'type': 'float',
                    'description' : "part of remaining power interp. as absorption"
                },
               "pgiter": { 
                    'title' : 'pgiter',
                    'value' : 1.e-4, 
                    'type': 'float',
                    'description' : "relative accuracy to stop iterations"
                },
                "ni1": { 
                    'title' : 'ni1',
                    'value' : 20, 
                    'type': 'int',
                    'description' : "grid number in the left part of Vz plato"
                },
                "ni2": { 
                    'title' : 'ni2',
                    'value' : 20, 
                    'type': 'int',
                    'description' : "grid number in the right part of Vz plato"
                },
                "niterat": { 
                    'title' : 'niterat',
                    'value' : 99, 
                    'type': 'int',
                    'description' : "maximal number of iterations"
                },                
                "nmaxm(1)": { 
                    'title' : 'nmaxm(1)',
                    'value' : 20, 
                    'type': 'int',
                    'description' : "permitted reflections at 0 iteration"
                },                
                "nmaxm(2)": { 
                    'title' : 'nmaxm(2)',
                    'value' : 20, 
                    'type': 'int',
                    'description' : "permitted reflections at 2 iteration"
                },                
                "nmaxm(3)": { 
                    'title' : 'nmaxm(3)',
                    'value' : 20, 
                    'type': 'int',
                    'description' : "permitted reflections at 3 iteration"
                },                
                "nmaxm(4)": { 
                    'title' : 'nmaxm(4)',
                    'value' : 20, 
                    'type': 'int',
                    'description' : "permitted reflections at 4 iteration"
                },                
                "maxstep2": { 
                    'title' : 'maxstep2',
                    'value' : 1000, 
                    'type': 'int',
                    'description' : "maximal steps' number in Fast comp. mode"
                },                
                "maxstep4": { 
                    'title' : 'maxstep4',
                    'value' : 1000, 
                    'type': 'int',
                    'description' : "maximal steps' number in Slow comp. mode"
                },                                                
            },

    
            "Options" :{
                   "ipri": { 
                    'title' : 'ipri',
                    'value' : 2, 
                    'type': 'int',
                    'description' : "printing output monitoring: 0,1,2,3,4']"
                },
                   "iw": { 
                    'title' : 'iw',
                    'value' : 1, 
                    'type': 'int',
                    'description' : "initial mode (slow=1, fast=-1)"
                },
                   "ismth": { 
                    'title' : 'ismth',
                    'value' : 1, 
                    'type': 'int',
                    'description' : "if=0, no smoothing in Ne(rho),Te(rho),Ti(rho)"
                },
                   "ismthalf": { 
                    'title' : 'ismthalf',
                    'value' : 0, 
                    'type': 'int',
                    'description' : "if=0, no smoothing in D_alpha(vperp)"
                },
                   "ismthout": { 
                    'title' : 'ismthout',
                    'value' : 1, 
                    'type': 'int',
                    'description' : "if=0, no smoothing in output profiles"
                },
                   "inew": { 
                    'title' : 'inew',
                    'value' : 0, 
                    'type': 'int',
                    'description' : "inew=0 for usual tokamak&Ntor_grill; 1 or 2 for g' in ST&Npol_grill"
                },
                   "itor": { 
                    'title' : 'itor',
                    'value' : 1, 
                    'type': 'int',
                    'description' : "+-1, Btor direction in right coord{drho,dteta,dfi}"
                },
                   "ipol": { 
                    'title' : 'ipol',
                    'value' : 1, 
                    'type': 'int',
                    'description' : "+-1, Bpol direction in right coord{drho,dteta,dfi}"
                },
            },
            'grill parameters':{
                   "Zplus": { 
                    'title' : 'Zplus',
                    'value' : 11, 
                    'type'  : 'float',
                    'unit'  : 'cm',
                    'description' : "upper grill corner in centimeters"
                }, 
                   "Zminus": { 
                    'title' : 'Zminus',
                    'value' : -11, 
                    'type': 'float',
                    'unit'  : 'cm',                    
                    'description' : "lower grill corner in centimeters"
                }, 
                   "ntet": { 
                    'title' : 'ntet',
                    'value' : 21, 
                    'type': 'int',
                    'description' : "theta grid number"
                },
                   "nnz": { 
                    'title' : 'nnz',
                    'value' : 51, 
                    'type': 'int',
                    'description' : "iN_phi grid number"
                }
            }
        }

    
class RTModel(BaseModel):
    """Ray tracing model"""
    def __init__(self, name= None, path= None) -> None:
        if name:
            super().__init__(name)
        if path:
            super().__init__(path.stem)
            self.path = path
            if self.path.exists():
                self.load()
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

    def load(self):
        with self.path.open("r") as json_file:
            self.data = json.load(json_file)

    def save_to_json(self):
        print('save_to_json:')
        print(self.path)
        #self.path.unlink()
        with self.path.open(mode= "w") as json_file:
            json.dump(self.data, json_file, indent=2)

    def get_text(self):
        #return 'test ray_tracing data'
        return self.prepare_dat_file()

    def get_dest_path(self):
        return os.path.join('lhcd', 'ray_tracing.dat')

    def prepare_dat_file(self):
        lines = []
        def item_to_line(item):
            name = item['title']
            vs = str(item['value'])
            v2 = item['description']
            return '  ' + vs + ' '*(9-len(vs)) + "  ! " + name + ' '*(15-len(name)) + v2 + '\n'

        for section_name, items in self.setting.items():
            if 'value' in items:
                continue
            if section_name == "spectrum":
                print('prepare: '+ section_name)      
                #lines += prepare_spectrum()
            else:
                #print('section: '+ section_name)  
                #print(items)
                lines.append("!"*15 + " "+ section_name + " "+ "!"*(60-len(section_name)) + "\n")
                lines += [ item_to_line(item) for name, item in items.items() if name !='total_power']
                
        spect = SpectrumModel(self.setting)
        spect_line = ''
        match spect.spectrum_type:
            case 'gaussian'| 'spectrum_1D':
                spect_line = '  1     ! spectr type 1 - 1D, 2 - 2D, 3 - scatter'
            case 'scatter_spectrum':
                spect_line = '  3     ! spectr type 1 - 1D, 2 - 2D, 3 - scatter'
            case 'spectrum_2D':
                spect_line = '  2     ! spectr type 1 - 1D, 2 - 2D, 3 - scatter'

        lines += spect_line   
        return ''.join(lines)        

    def get_spectrum_model(self):
        return SpectrumModel(self.setting)