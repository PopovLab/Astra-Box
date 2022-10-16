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
    def __init__(self, parent) -> None:
        if not 'spectrum' in parent:
            parent['spectrum'] = defaultGaussSetting()
        self.setting = parent['spectrum']
        self.power = parent['grill parameters']['total_power']['value']

    def generate(self):
        options = self.setting['options']
        x = np.arange(options['x_min'], options['x_max'], options['step'])
        bias = options['bias']
        sigma = options['sigma']
        y = np.exp(-0.5*((x-bias)/sigma)**2) # + np.exp(-25*((x+bias)/bias)**2)
        self.spectrum_data = { 'Ntor': x.tolist(), 'Amp': y.tolist()  }        

    def divide_spectrum(self):
        sp = [x for x in zip(self.spectrum_data['Ntor'], self.spectrum_data['Amp'])]
        sp_pos = [ (s[0], s[1]) for s in sp if s[0]>0]
        sp_neg = [ (-s[0], s[1]) for s in sp if s[0]<0]
        sp_neg = list(reversed(sp_neg))
        return sp_pos, sp_neg

    def get_text(self):
        self.generate()
        out_lines = []
        sp_pos, sp_neg = self.divide_spectrum()
        out_lines.append("!!positive Nfi; P_LH(a.units); points<1001\n")
        for s in sp_pos:
            out_lines.append(str(s[0]) + "   " + str(s[1])+"\n")
        #print(len(out_lines))

        #power = parameters['grill parameters']['total power'][0]
        out_lines.append(str(self.power) + '	-88888. !0.57 first value=part(%) of total power in positive spectrum.\n')
        out_lines.append('!!negative Nfi; P_LH(a.units); points number<1001, arbitrary spacing.\n')

        for s in sp_neg:
            out_lines.append(str(s[0]) + "   " + str(s[1])+"\n")
        #print(len(out_lines))
        return out_lines