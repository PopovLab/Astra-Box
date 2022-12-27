import numpy as np
import os

def defaultGaussSpectrum():
    return {
        'spectrum_type': 'gaussian',
        'options':{
            'x_min' : -40.0,
            'x_max' : 40.0,
            'step'  : 0.25,
            'bias'  : 10,
            'sigma' : 2.5
        }
    }

def defaulSpectrum1D():
    return {
        'spectrum_type': 'spectrum_1D',
        'source': ''
    }    

def defaulSpectrum2D():
    return {
        'spectrum_type': 'spectrum_2D',
        'source': ''
    }

class SpectrumModel():
    def __init__(self, parent) -> None:
        self.parent = parent
        if not 'spectrum' in parent:
            self.spectrum_type = 'gaussian'
        self.setting = self.parent['spectrum']
        self.positive_power = 0 

    def get_ratio_content(self):
        return [('Spectrum 2D', 'spectrum_2D'), ('Spectrum 1D', 'spectrum_1D'), ('Gaussian spectrum', 'gaussian')]



    @property
    def spectrum_type(self):
        return self.parent['spectrum']['spectrum_type']

    @spectrum_type.setter
    def spectrum_type(self, value):
        match value:
            case 'gaussian':
                self.parent['spectrum'] = defaultGaussSpectrum()
            case 'spectrum_1D':
                self.parent['spectrum'] = defaulSpectrum1D()
            case 'spectrum_2D':
                self.parent['spectrum'] = defaulSpectrum2D()
        self.setting = self.parent['spectrum']




    def read_spcp1D(self):        
        file_path = self.setting['source']
        if os.path.exists(file_path):
            file = open(file_path)
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
            self.spectrum_data = spectrum 
        else:
            self.spectrum_data = { 'Ntor': [], 'Amp': []  }
        self.spectrum_normalization()            
  
    def read_spcp2(self):
        file_path = self.setting['source']
        if os.path.exists(file_path):
            file = open(file_path)
            table = []
            header = file.readline().split()
            print(header)
            spectrum1D = { h: [] for h in header }
            lines = file.readlines()    
            for line in lines:
                table.append(line.split())
            for row in table:
                for index, (p, item) in enumerate(spectrum1D.items()):
                    item.append(float(row[index]))
    
            Nz_v = spectrum1D['Nz'][0]
            Ny_v = spectrum1D['Ny'][0]
            spectrum_shape = (spectrum1D['Nz'].count(Nz_v),spectrum1D['Ny'].count(Ny_v) )
            print(spectrum_shape)
            spectrum2D = { h: [] for h in header }
            for key, item in spectrum1D.items():
                spectrum2D[key] = np.ndarray(shape=spectrum_shape, buffer=np.array(item) )# dtype=float, order='F')
        
            level = 0.4
            arr = spectrum2D['Px']
            with np.nditer(arr, op_flags=['readwrite']) as it:
                for x in it:
                    x[...] = x if x<level else level
            self.spectrum_data = spectrum2D   
        else:
            self.spectrum_data = None


    def make_gauss_data(self):
        options = self.setting['options']
        x = np.arange(options['x_min'], options['x_max'], options['step'])
        bias = options['bias']
        sigma = options['sigma']
        y = np.exp(-0.5*((x-bias)/sigma)**2) # + np.exp(-25*((x+bias)/bias)**2)
        self.spectrum_data = { 'Ntor': x.tolist(), 'Amp': y.tolist()  }        
        self.spectrum_normalization()
    
    def spectrum_normalization(self):
        power = 0
        positive_power = 0
        for x, y  in zip(self.spectrum_data['Ntor'], self.spectrum_data['Amp']):
            power += y
            if x>0: positive_power += y
        self.spectrum_data['Amp'] = [ x/power for x in self.spectrum_data['Amp']]
        print(f'{power} {positive_power}')
        self.positive_power = positive_power /power

    def generate(self):
        match self.spectrum_type:
            case 'gaussian':
                self.make_gauss_data()
            case 'spectrum_1D':
                self.read_spcp1D()
            case 'spectrum_2D':
                self.read_spcp2D()

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
        out_lines.append(f'{self.positive_power:.4f} -88888. !0.57 first value=part(%) of total power in positive spectrum.\n')
        out_lines.append('!!negative Nfi; P_LH(a.units); points number<1001, arbitrary spacing.\n')

        for s in sp_neg:
            out_lines.append(str(s[0]) + "   " + str(s[1])+"\n")
        #print(len(out_lines))
        return out_lines