import os 
from pathlib import Path
import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
from tkinter import filedialog as fd
from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import ( FigureCanvasTkAgg, NavigationToolbar2Tk)
from AstraBox import UIElement, WorkSpace
from AstraBox.Models.Spectrum import BaseSpectrum, GaussSpectrum, ScatterSpectrum, Spectrum1D, Spectrum2D
from AstraBox.ToolBox.SpectrumPlot import ScatterPlot
from AstraBox.ToolBox.SpectrumPlot import RotatedSpectrumPlot
from AstraBox.ToolBox.SpectrumPlot import ScatterPlot3D
from AstraBox.ToolBox.SpectrumPlot import Plot2DArray
from AstraBox.ToolBox.SpectrumPlot import SpectrumPlot
from AstraBox.ToolBox.SpectrumPlot import ScatterPlot2D3D
from AstraBox.Models.SpectrumModel_v2 import SpectrumModel
import AstraBox.Widgets as Widgets


class OptionsPanel(tk.Frame):
    def __init__(self, master, section: BaseSpectrum, state:str= 'normal' ) -> None:
            super().__init__(master)
            self.section = section
            count=0
            schema= section.model_json_schema()['properties']
            print(schema)
            UIElement.LABEL_WIDTH = None
            for name, value in section:
                print(name)
                if name != 'kind':
                    e = UIElement.construct(self, name, value, schema[name], self.observer, state)
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
        btn.grid(row=3, column=1, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W)  
        self.columnconfigure(0, weight=1)        
        #self.rowconfigure(0, weight=1)    
        self.generate()
        self.rowconfigure(2, weight=1)

    def generate(self):
        #self.options_box.update()
        s_d= self.model.spectrum.get_spectrum_data()
        self.spectrum_plot = SpectrumPlot(self, s_d['Ntor'], s_d['Amp']  )
        self.spectrum_plot.grid(row=1, column=0, rowspan=12,  padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W)  


class FileSourcePanel(tk.Frame):
    def __init__(self, master, spectrum:GaussSpectrum | Spectrum1D | Spectrum2D | ScatterSpectrum , on_select_source = None) -> None:
        super().__init__(master)
        self.spectrum_folder = WorkSpace.get_location_path() / 'spectrum_data'
        print(self.spectrum_folder)
        self.on_select_source = on_select_source
        self.path_var = tk.StringVar(master= self, value=spectrum.source)
        label = tk.Label(master=self, text='Source:')
        label.pack(side = tk.LEFT, padx=2)		
        entry = tk.Entry(self, width=65, textvariable= self.path_var)
        entry.pack(side = tk.LEFT, padx=2)
        btn1 = ttk.Button(self, text= 'Select file', command=self.select_file)
        btn1.pack(side = tk.LEFT, padx=10)   

    def load_file(self):
        if self.on_select_source:
            self.on_select_source(self.path_var.get())

    def select_file(self):
        filename = fd.askopenfilename(initialdir= self.spectrum_folder)
        if len(filename) < 1 : return
        fp = Path(filename)
        if fp.is_relative_to(self.spectrum_folder):
            filename = fp.name
        if self.on_select_source:
            if self.on_select_source(filename):
                self.path_var.set(filename)


class Spectrum1DView(tk.LabelFrame):
    def __init__(self, master, model=None) -> None:
        super().__init__(master, text='Spectrum 1D')        

        self.model = model
        self.label = ttk.Label(self,  text=f'Spectrum View')
        self.label.grid(row=0, column=0, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W)  

        self.control_panel = FileSourcePanel(self, self.model.spectrum, self.on_load_file)
        self.control_panel.grid(row=0, column=0, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W) 

        self.options_box = OptionsPanel(self, self.model.spectrum)
        self.options_box.grid(row=1, column=0, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W) 
        #btn = ttk.Button(self, text= 'Generate', command=self.generate)
        #btn.grid(row=3, column=1, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W)  
        self.columnconfigure(0, weight=1)        
        #self.rowconfigure(0, weight=1)    
        self.make_plot()
        self.rowconfigure(2, weight=1)        

    def on_load_file(self, filename):
        print(filename)
        self.model.spectrum.source = filename
        self.make_plot()        

    def make_plot(self):
        try:
            spectrum_data = self.model.spectrum.get_spectrum_data()
        except Exception as e :
            ex_text= f"{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: \n{e}"
            label = ttk.Label(self, text= ex_text, width=20)
            label.grid(row=3, column=0, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W)       
        else:
            self.spectrum_plot = SpectrumPlot(self, spectrum_data['Ntor'], spectrum_data['Amp']  )
            self.spectrum_plot.grid(row=2, column=0,  rowspan=3, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W)         

class Spectrum2DView(tk.LabelFrame):
    def __init__(self, master, model:SpectrumModel ) -> None:
        super().__init__(master, text='Spectrum 2D')        
        self.spectrum_data = None
        self.model = model
        self.numper_points = tk.IntVar(self, value=0) 
        self.label = ttk.Label(self,  text=f'Spectrum View')
        self.label.grid(row=0, column=0, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W)  

        self.control_panel = FileSourcePanel(self, self.model.spectrum, self.on_set_file_name)
        self.control_panel.grid(row=0, column=0, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W) 

        #self.options_box = OptionsPanel(self, self.model.spectrum)
        #self.options_box.grid(row=1, column=0, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W) 

        level_pabel= self.make_level_panel()
        level_pabel.grid(row=2, column=0, sticky=tk.W)

        spectrum_data = self.model.spectrum.get_spectrum_data()
        if spectrum_data:
            self.numper_points.set(spectrum_data['Nz'].size)
            self.spectrum_plot = Plot2DArray(self, spectrum_data)
            self.spectrum_plot.grid(row=3, column=0, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W)  
        else:
            label = ttk.Label(self, text= "Ошибка загрузки спектра", width=20)
            label.grid(row=3, column=0, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W)             
        self.columnconfigure(0, weight=1)        
        self.rowconfigure(3, weight=1)        

    def make_level_panel(self):
        panel = tk.Frame(self)
        tk.Label(panel, text="Cut level").pack(side=tk.LEFT, padx=6, pady=6)
        self.level_var = tk.DoubleVar(self, value=0.0) 
        tk.Entry(panel, width=20, textvariable= self.level_var).pack(side=tk.LEFT, padx=6, pady=6)        
        ttk.Button(panel, text='Update Level', command= self.update_level).pack(side=tk.LEFT, padx=6, pady=6)
        tk.Label(panel, text="Number of points").pack(side=tk.LEFT, padx=6, pady=6)
        tk.Entry(panel, width=10, textvariable= self.numper_points, state='readonly').pack(side=tk.LEFT, padx=6, pady=6)        
        ttk.Button(panel, text='Export to file', command= self.export_to_file).pack(side=tk.LEFT, padx=6, pady=6)
        return panel
    
    def update_level(self):
        np = self.spectrum_plot.update_level(self.level_var.get())
        self.numper_points.set(np)

    def export_to_file(self):
        self.spectrum_plot.export_to_file(self.level_var.get())

    def on_set_file_name(self, filename:str) -> bool:
        spectrum_data = self.model.spectrum.get_spectrum_data(filename)
        if spectrum_data:
            self.spectrum_plot = Plot2DArray(self, spectrum_data)
            self.spectrum_plot.grid(row=1, column=0, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W)        
            return True
        else:
            return False

        
class ScatterSpectrumView(tk.LabelFrame):
    def __init__(self, master, model=None) -> None:
        super().__init__(master, text='Scatter Spectrum')        
        
        self.model = model
        spectrum_data = self.model.spectrum.get_spectrum_data()
        self.numper_points = tk.IntVar(self, value=len(spectrum_data['Amp'])) 
        self.control_panel = FileSourcePanel(self, self.model.spectrum, self.on_load_file)
        self.control_panel.grid(row=0, column=0, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W) 

        level_panel = self.make_level_panel()
        level_panel.grid(row=1, column=0, columnspan=2, sticky=tk.W)  

        if spectrum_data:
            self.spectrum_plot = ScatterPlot2D3D(self, spectrum_data)
            self.spectrum_plot.grid(row=2, column=0, columnspan= 2, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W)             

        self.columnconfigure(0, weight=1)        
        self.rowconfigure(2, weight=1)    
 
    def on_load_file(self, filename):
        print(filename)
        spectrum_data = self.model.spectrum.get_spectrum_data(filename)
        if spectrum_data:
            self.spectrum_plot = ScatterPlot2D3D(self, spectrum_data)
            self.spectrum_plot.grid(row=2, column=0, columnspan= 2, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W) 
            return True
        else:
            return False

    def make_level_panel(self):
        panel = tk.Frame(self)
        tk.Label(panel, text="Cut level").pack(side=tk.LEFT, padx=6, pady=6)
        self.level_var = tk.DoubleVar(self, value=0.0) 
        tk.Entry(panel, width=20, textvariable= self.level_var).pack(side=tk.LEFT, padx=6, pady=6)        
        ttk.Button(panel, text='Update Level', command= self.update_level).pack(side=tk.LEFT, padx=6, pady=6)
        tk.Label(panel, text="Number of points").pack(side=tk.LEFT, padx=6, pady=6)
        tk.Entry(panel, width=10, textvariable= self.numper_points, state='readonly').pack(side=tk.LEFT, padx=6, pady=6)        
        ttk.Button(panel, text='Save file', command= self.save_file).pack(side=tk.LEFT, padx=6, pady=6)
        return panel
    
    def update_level(self):
        cut_level = self.level_var.get()
        print(cut_level)
        np = self.spectrum_plot.update_level(cut_level)
        self.numper_points.set(np)

    def save_file(self):
        cut_level = self.level_var.get()
        print(cut_level)
        self.spectrum_plot.save_file(cut_level)