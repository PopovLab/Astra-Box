import numpy as np
import os
from math import fsum

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

def defaulScatterSpectrum():
    return {
        'spectrum_type': 'scatter_spectrum',
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

    def get_dest_path(self):
        #return os.path.join('lhcd', 'spectrum.dat')
        return 'lhcd/spectrum.dat'

    def get_radio_content(self):
        return [('Spectrum 2D', 'spectrum_2D'), ('Scatter Spectrum', 'scatter_spectrum'), ('Spectrum 1D', 'spectrum_1D'), ('Gaussian spectrum', 'gaussian')]


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
            case 'scatter_spectrum':
                self.parent['spectrum'] = defaulScatterSpectrum()                
            case 'spectrum_2D':
                self.parent['spectrum'] = defaulSpectrum2D()
        self.setting = self.parent['spectrum']

    def read_scatter(self, filepath):
        if os.path.exists(filepath):
            with open(filepath) as file:
                self.read_data(file)
        else:
            self.spectrum_data = None

    def read_data(self, file):
        data = { 'Ntor': [], 'Npol': [], 'Amp':[]}
        lines = file.readlines()
        table = []
        for line in lines:
            #if isBlank(line): break
            #print(line)
            if type(line) is str:
                table.append(line.split())    
            else:                
                table.append(line.decode("utf-8").split())
        #print(len(table))
        for row in table:
            for index, (p, item) in enumerate(data.items()):
                #print(p, item, index)
                try:
                    item.append(float(row[index]))
                except ValueError:
                    item.append(0.0)
        self.spectrum_data = data

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
  
    def read_spcp2D(self, file_path):
        #file_path = self.setting['source']
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
            arr = spectrum2D['Amp']
            with np.nditer(arr, op_flags=['readwrite']) as it:
                for x in it:
                    x[...] = x if x<level else level
            self.spectrum_data = spectrum2D   
        else:
            self.spectrum_data = None


    def make_gauss_data(self):
        options = self.setting['options']
        num = int((options['x_max'] - options['x_min'])/options['step'])
        x = np.linspace(options['x_min'], options['x_max'], num = num)
        bias = options['bias']
        sigma = options['sigma']
        y = np.exp(-0.5*((x-bias)/sigma)**2) # + np.exp(-25*((x+bias)/bias)**2)
        self.spectrum_data = { 'Ntor': x.tolist(), 'Amp': y.tolist()  }        
        self.spectrum_normalization()
    
    def spectrum_normalization(self):
        power = fsum(self.spectrum_data['Amp'])
        positive_power = fsum([x[1] for x in zip(self.spectrum_data['Ntor'], self.spectrum_data['Amp']) if x[0]>0])
        self.spectrum_data['Amp'] = [ x/power for x in self.spectrum_data['Amp']]
        self.positive_power = positive_power /power
  

    def generate(self):
        match self.spectrum_type:
            case 'gaussian':
                self.make_gauss_data()
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

    def get_text(self):
        self.generate()
        print(self.spectrum_type)
        match self.spectrum_type:
            case 'gaussian'| 'spectrum_1D':
                sp = [(x,0,p) for x, p in zip(self.spectrum_data['Ntor'], self.spectrum_data['Amp'])]
            case 'scatter_spectrum':
                sp = [(x,y,p) for x, y, p  in zip(self.spectrum_data['Ntor'], self.spectrum_data['Npol'], self.spectrum_data['Amp'])]                                
            case 'spectrum_2D':
                sp = [(x,y,p) for x, y, p  in zip(self.spectrum_data['Nz'], self.spectrum_data['Ny'], self.spectrum_data['Amp'])]                
        return ''.join([f'{s[0]:.5f}  {s[1]:.5f}  {s[2]}\n' for s in sp])

    def get_text_div_spectrum(self):
        self.generate()
        sp_pos, sp_neg = self.divide_spectrum()
        text1 = "!!positive Nfi; P_LH(a.units); points<1001\n"
        pos_lines = [f'{s[0]:.5f}   {s[1]}\n' for s in sp_pos]

        #power = parameters['grill parameters']['total power'][0]
        text2 = f'{self.positive_power:.4f} -88888. !0.57 first value=part(%) of total power in positive spectrum.\n'
        text3 = '!!negative Nfi; P_LH(a.units); points number<1001, arbitrary spacing.\n'

        neg_lines = [f'{s[0]:.5f}   {s[1]}\n' for s in sp_neg]
        #print(len(out_lines))
        return [text1, *pos_lines, text2, text3, *neg_lines]