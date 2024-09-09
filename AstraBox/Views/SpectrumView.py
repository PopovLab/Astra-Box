import os 
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog as fd
from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import ( FigureCanvasTkAgg, NavigationToolbar2Tk)
from AstraBox import UIElement
from AstraBox.Models.Spectrum import BaseSpectrum
from AstraBox.ToolBox.SpectrumPlot import ScatterPlot
from AstraBox.ToolBox.SpectrumPlot import RotatedSpectrumPlot
from AstraBox.ToolBox.SpectrumPlot import ScatterPlot3D
from AstraBox.ToolBox.SpectrumPlot import Plot2DArray
from AstraBox.ToolBox.SpectrumPlot import SpectrumPlot
from AstraBox.ToolBox.SpectrumPlot import ScatterPlot2D3D

import AstraBox.Widgets as Widgets


class OptionsPanel(tk.Frame):
    def __init__(self, master, section: BaseSpectrum ) -> None:
            super().__init__(master)
            self.section = section
            count=0
            schema= section.model_json_schema()['properties']
            for name, value in section:
                e = UIElement.construct(self, name, value, schema[name], self.observer)
                e.grid(row=0, column= count, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)
                count = count + 1

    def observer(self, name, value):
        print(f'{name} {value}')
        setattr(self.section, name, value)

class GaussianSpectrumView(tk.LabelFrame):
    def __init__(self, master, model=None) -> None:
        super().__init__(master, text='Gaussian Spectrum')        

        self.model = model
        self.label = ttk.Label(self,  text=f'Spectrum View')
        self.label.grid(row=0, column=0, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W)  

        self.options_box = OptionsPanel(self, self.model.spectrum)
        self.options_box.grid(row=0, column=0, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W) 
        btn = ttk.Button(self, text= 'Generate', command=self.generate)
        btn.grid(row=0, column=1, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W)  
        self.columnconfigure(0, weight=1)        
        #self.rowconfigure(0, weight=1)    
        self.generate()
        #wg1 = Widgets.create_widget(self, self.model.setting['parameters']['angle'])
        #wg1.grid(row=1, column=1, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)
        #wg2 = Widgets.create_widget(self, self.model.setting['parameters']['spline'])
        #wg2.grid(row=1, column=1, padx=5, sticky=tk.N)

        self.rowconfigure(2, weight=1)

    def generate(self):
        #self.options_box.update()
        s_d= self.model.spectrum.make_spectrum_data()
        self.spectrum_plot = SpectrumPlot(self, s_d['Ntor'], s_d['Amp']  )
        self.spectrum_plot.grid(row=1, column=0, rowspan=12,  padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W)  