import numpy as np

def defaultGaussSetting():
    return {
        'spectrum_type': 'Gaussian',
        'options':{
            'x_min' : -40.0,
            'x_max' : 40.0,
            'step'  : 0.25,
            'bias'  : 10,
            'sigma' : 2.5
        }
    }

class SpectrumModel():
    def __init__(self) -> None:
        self.setting = defaultGaussSetting()

    def generate(self):
        options = self.setting['options']
        x = np.arange(options['x_min'], options['x_max'], options['step'])
        bias = options['bias']
        sigma = options['sigma']
        y = np.exp(-0.5*((x-bias)/sigma)**2) # + np.exp(-25*((x+bias)/bias)**2)
        self.spectrum_data = { 'Ntor': x.tolist(), 'Amp': y.tolist()  }        

