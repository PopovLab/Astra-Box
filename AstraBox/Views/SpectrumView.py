import os 
from pathlib import Path
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog as fd
from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import ( FigureCanvasTkAgg, NavigationToolbar2Tk)
from AstraBox import UIElement, WorkSpace
from AstraBox.Models.Spectrum import BaseSpectrum, Spectrum1D
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
            print(schema)
            for name, value in section:
                print(name)
                if name != 'kind':
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
        btn.grid(row=3, column=1, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W)  
        self.columnconfigure(0, weight=1)        
        #self.rowconfigure(0, weight=1)    
        self.generate()
        self.rowconfigure(2, weight=1)

    def generate(self):
        #self.options_box.update()
        s_d= self.model.spectrum.make_spectrum_data()
        self.spectrum_plot = SpectrumPlot(self, s_d['Ntor'], s_d['Amp']  )
        self.spectrum_plot.grid(row=1, column=0, rowspan=12,  padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W)  


class FileSourcePanel(tk.Frame):
    def __init__(self, master, spectrum:Spectrum1D , on_select_source = None) -> None:
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
        self.path_var.set(filename)
        if self.on_select_source:
            self.on_select_source(filename)


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
        spectrum_data = self.model.spectrum.read_spcp1D()
        self.spectrum_plot = SpectrumPlot(self, spectrum_data['Ntor'], spectrum_data['Amp']  )
        self.spectrum_plot.grid(row=2, column=0,  rowspan=3, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W)         

class Spectrum2DView(tk.LabelFrame):
    def __init__(self, master, model=None) -> None:
        super().__init__(master, text='Spectrum 2D')        

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
        spectrum_data = self.model.spectrum.spectrum_data()
        if spectrum_data == None:
            label = ttk.Label(self, text="Spectrum None", width=20)
            label.grid(row=1, column=0, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W)       
            return False
        else:
            self.spectrum_plot = Plot2DArray(self, spectrum_data)
            self.spectrum_plot.grid(row=1, column=0, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W)  
            return True
        
class ScatterSpectrumView(tk.LabelFrame):
    def __init__(self, master, model=None) -> None:
        super().__init__(master, text='Scatter Spectrum')        

        self.model = model

        self.control_panel = FileSourcePanel(self, self.model.spectrum, self.on_load_file)
        self.control_panel.grid(row=0, column=0, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W) 

        radio_selector = self.make_radio_selector()
        radio_selector.grid(row=0, column=1, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W) 
        self.columnconfigure(0, weight=1)        
        #self.rowconfigure(0, weight=1)    
        self.make_plot()

    def on_load_file(self, filepath):
        print(filepath)
        self.model.spectrum.source = filepath
        self.make_plot(filepath)
            

    def make_plot(self):
        #head, filename = os.path.split(filepath)
        return self.make_scatter_plot3D()

    def make_scatter_plot3D(self):
        self.spectrum_data = self.model.spectrum.read_scatter()
            
        if self.spectrum_data == None:
            print('spectrum_data == None')
            label = ttk.Label(self, text="Spectrum None", width=20)
            label.grid(row=1, column=0, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W)       
            return False
        else:
            self.spectrum_plot = ScatterPlot2D3D(self, self.spectrum_data)
            self.spectrum_plot.grid(row=1, column=0, columnspan= 2, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W)  
            return True

    def make_radio_selector(self):
        frame = ttk.Frame(self, relief=tk.FLAT)
        # border=border, borderwidth, class_, cursor, height, name, padding, relief, style, takefocus, width)
        padx = 10
        pady = 5
        btn2 = ttk.Radiobutton(frame, text='3D', value='3D', width=5, 
                                command= self.select_View3D,
                                style= 'Toolbutton')
        btn2.pack(side=tk.RIGHT, padx=padx, pady=pady)

        btn1 = ttk.Radiobutton(frame, text='2D',  value='2D', width=5, 
                                command= self.select_View2D,
                                style= 'Toolbutton')
        btn1.pack(side=tk.RIGHT, padx=padx, pady=pady)
        return frame

    def select_View2D(self):
        self.spectrum_plot = ScatterPlot2D3D(self, self.spectrum_data)
        self.spectrum_plot.grid(row=1, column=0, columnspan= 2, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W)  

    def select_View3D(self):
        self.spectrum_plot = ScatterPlot3D(self, self.spectrum_data)
        self.spectrum_plot.grid(row=1, column=0, columnspan= 2, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W)           