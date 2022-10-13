import numpy as np

def defaultGaussSetting():
    return {
        'type': 'gauss',
        'range': {
            'x_min' : -40.0,
            'x_max' : 40.0,
            'step'  : 0.25,
            'bias'  : 10
        }
    }

class SpectrumModel():
    def __init__(self) -> None:
        self.setting = defaultGaussSetting()

    def generate(self):
        x = np.arange(-40, 40, 0.25)
        bias = 10
        y = np.exp(-25*((x-bias)/bias)**2) # + np.exp(-25*((x+bias)/bias)**2)
        self.spectrum_data = { 'Ntor': x.tolist(), 'Amp': y.tolist()  }        

