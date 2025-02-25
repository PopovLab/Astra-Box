import tkinter as tk
import tkinter.ttk as ttk

import numpy as np
import pandas as pd

from AstraBox.Models.RaceModel import RaceModel
from AstraBox.RaceTab.TabViewBasic import TabViewBasic
from AstraBox.ToolBox.SpectrumPlot import SpectrumChart, ScatterPlot2D3D
from AstraBox.Views.SheetView import SheetView
from AstraBox.Views.SpectrumView import OptionsPanel

class SpectrumTabView(TabViewBasic):
    
    def __init__(self, master, model: RaceModel) -> None:
        super().__init__(master, model)  

    def init_ui(self):
        print('create SpectrumView')
        self.spectrums = {}

        self.spectrums['origin'] = self.read_spectrum('spectrum.dat')
        self.spectrums['full_spectrum'] = self.read_spectrum('full_spectrum.dat')        
        self.spectrums['spectrum_pos'] = self.read_spectrum('spectrum_pos.dat')
        self.spectrums['spectrum_neg'] = self.read_spectrum('spectrum_neg.dat')        

        self.nteta =  self.race_model.frtc_model.grill_parameters.ntet
        #self.spectrums['nteta'] = self.nteta
        spectrum_kind = self.race_model.spectrum_model.spectrum.kind
       
        if self.spectrums['origin'] is None:
            plot = tk.Label(master=self, text='Нет данных')
        else:
            plot = self.make_spectrum_plot(spectrum_kind)
        plot.grid(row=0, column=0, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)
        

        options_box = OptionsPanel(self, self.race_model.spectrum_model.spectrum, state='disabled')
        options_box.grid(row=1, column=0, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W) 
        
        txt = self.make_summary()
        txt.grid(row=2, column=0, padx=4, pady=4, sticky=tk.N + tk.S + tk.E + tk.W)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
    
    def read_spectrum(self, fname):
        spectr = self.race_model.read_dat_no_header(f'lhcd/{fname}')
        if spectr is not None:
            spectr=  spectr.set_axis(['Ntor', 'Npol', 'Amp'], axis=1)
            if spectr['Ntor'][0] > spectr['Ntor'].iat[-1]:
                spectr = spectr.iloc[::-1]
                
            return spectr
        else:
            return None
        
    def make_frtc_summary(self):
        frtc = self.race_model.frtc_model
        
        text = "------- FRTC parameters ----------\n"
        text +=  f"Freq: {frtc.physical_parameters.freq} "
        text +=  f"nr: {frtc.numerical_parameters.nr} "
        text +=  f"eps: {frtc.numerical_parameters.eps} \n"
        text +=  f"Zplus: {frtc.grill_parameters.Zplus} "
        text +=  f"Zminus: {frtc.grill_parameters.Zminus} "
        text +=  f"ntet: {frtc.grill_parameters.ntet} "
        text +=  f"nnz: {frtc.grill_parameters.nnz}"
        return text
    
    def make_spectrum_plot(self, spectrum_kind):
        match spectrum_kind:
            case 'gauss_spectrum'|'spectrum_1D':
                plot = SpectrumChart(self, self.spectrums, self.nteta, show_summary=False)
            case 'scatter_spectrum'|'rotated_gaussian':
                plot = ScatterPlot2D3D(self, self.spectrums['origin'])
            case 'spectrum_2D':
                pass       
        return plot
    
    def make_spectrum_statistic(self):
        xsgs = 1e+13 # 1MW = 1e13 erg/s ( 1 mega watts)
        d = {}
        for key, s in self.spectrums.items():
            print('-----------')
            print(key)
            if s is not None:
                if type(s).__name__ == 'DataFrame':
                    print(type(s).__name__)
                    p = np.sum(s["Amp"])
                    r = s['Amp']
                    col = [r.size, p, f'{p/xsgs:.4f} MW', f'{self.nteta*p/xsgs:.4f} MW']
                else:
                    col = [s, '-', '-', '-']
                d[key] = pd.Series(col, index=["size", "sum", "beam", "total"])
        df = pd.DataFrame(d)

        return df.to_string(max_rows = 6) + '\n'

    def make_summary(self):
        text=  self.make_spectrum_statistic()

        text_box = tk.Text(self, height = 8, width = 50)
        text_box.insert(tk.END, text)
        text_box.insert(tk.END, self.make_frtc_summary())
        text_box.config(state='disabled')
        return text_box
    
