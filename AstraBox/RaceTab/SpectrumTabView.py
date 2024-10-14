import tkinter as tk
import tkinter.ttk as ttk

from AstraBox.Models.RaceModel import RaceModel
from AstraBox.RaceTab.TabViewBasic import TabViewBasic
from AstraBox.ToolBox.SpectrumPlot import SpectrumChart, ScatterPlot2D3D
from AstraBox.Views.SheetView import SheetView

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

        self.spectrums['nteta'] =  21 #self.rt['grill parameters']['ntet']['value']
        spectrum_kind = self.race_model.spectrum_model.spectrum.kind
       
        if self.spectrums['origin'] is None:
            plot = tk.Label(master=self, text='Нет данных')
        else:
            plot = self.make_spectrum_plot(spectrum_kind)
        plot.grid(row=1, column=0, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
    
    def read_spectrum(self, fname):
        spectr = self.race_model.read_dat_no_header(f'lhcd/{fname}')
        if spectr is not None:
            spectr=  spectr.set_axis(['Ntor', 'Npol', 'Amp'], axis=1)
            if spectr['Ntor'][0] > spectr['Ntor'].iat[-1]:
                spectr = spectr.iloc[::-1]
                
            return spectr
        else:
            return None
        
    def item_str(self, k1, k2):
        #print(self.rt)
        item = self.rt[k1][k2]
        return f"{item['title']}:  {item['value']}"
        #return f"{k1}:  {k2}"

    def make_summary_v1(self):
        #summ = tk.Label(master=self, text='Место для RT model')
        values = []
        values.append(self.item_str('Physical parameters', 'Freq'))
        values.append(self.item_str('Numerical parameters', 'nr'))
        values.append(self.item_str('Numerical parameters', 'eps'))
        values.append(self.item_str('Options', 'inew'))
        values.append(self.item_str('grill parameters', 'Zplus'))
        values.append(self.item_str('grill parameters', 'Zminus'))
        values.append(self.item_str('grill parameters', 'ntet'))
        values.append(self.item_str('grill parameters', 'nnz'))
        
        summ = SheetView(self, values)
        return summ
    
    def make_spectrum_plot(self, spectrum_kind):
        match spectrum_kind:
            case 'gaussian'|'spectrum_1D':
                #plot = SpectrumPlot(self, self.spectrum_model.spectrum_data['Ntor'], self.spectrum_model.spectrum_data['Amp']  )
                #plot = SpectrumPlot(self, spectrum_list= self.all_spectrum)
                plot = SpectrumChart(self, self.spectrums)
            case 'scatter_spectrum'|'rotated_gaussian':
                plot = ScatterPlot2D3D(self, self.spectrums['origin'])
            case 'spectrum_2D':
                pass       
        
        return plot