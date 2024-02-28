import os 
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog as fd
from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import ( FigureCanvasTkAgg, NavigationToolbar2Tk)
from AstraBox.ToolBox.SpectrumPlot import ScatterPlot
from AstraBox.ToolBox.SpectrumPlot import RotatedSpectrumPlot
from AstraBox.ToolBox.SpectrumPlot import ScatterPlot3D
from AstraBox.ToolBox.SpectrumPlot import Plot2DArray
from AstraBox.ToolBox.SpectrumPlot import SpectrumPlot
from AstraBox.ToolBox.SpectrumPlot import ScatterPlot2D3D
from AstraBox.Models.SpectrumModel import SpectrumModel

import AstraBox.Widgets as Widgets

class OptionsPanel(tk.Frame):
    def __init__(self, master, options) -> None:
        super().__init__(master)
        self.options = options
        for key, value in options.items():
            var = tk.DoubleVar(master= self, name = key, value=value)
            label = tk.Label(master=self, text=key)
            label.pack(side = tk.LEFT, padx=(10, 2))		
            entry = tk.Entry(self, width=10, textvariable= var)
            entry.pack(side = tk.LEFT)

    def update(self):
        for key in self.options.keys():
            var = tk.DoubleVar(master= self, name = key)
            self.options[key] = var.get()


class GaussianSpectrumView(tk.LabelFrame):
    def __init__(self, master, model=None) -> None:
        super().__init__(master, text='Gaussian Spectrum')        

        #self.header_content = { "title": 'title', "buttons":[('Save', None), ('Delete', None), ('Clone', None)]}
        self.model = model
        self.label = ttk.Label(self,  text=f'Spectrum View')
        self.label.grid(row=0, column=0, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W)  

        self.options_box = OptionsPanel(self, self.model.setting['options'])
        self.options_box.grid(row=0, column=0, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W) 
        btn = ttk.Button(self, text= 'Generate', command=self.generate)
        btn.grid(row=0, column=1, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W)  
        self.columnconfigure(0, weight=1)        
        #self.rowconfigure(0, weight=1)    
        self.generate()
        #wg1 = Widgets.create_widget(self, self.model.setting['parameters']['angle'])
        #wg1.grid(row=1, column=1, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)
        wg2 = Widgets.create_widget(self, self.model.setting['parameters']['spline'])
        wg2.grid(row=1, column=1, padx=5, sticky=tk.N)

        self.rowconfigure(2, weight=1)

    def generate(self):
        self.options_box.update()
        self.model.generate()
        self.spectrum_plot = SpectrumPlot(self, self.model.spectrum_data['Ntor'], self.model.spectrum_data['Amp']  )
        self.spectrum_plot.grid(row=1, column=0, rowspan=12,  padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W)  


class RotatedGaussianView(tk.LabelFrame):
    def __init__(self, master, model=None) -> None:
        super().__init__(master, text='Rotated Gaussian Spectrum')        
        self.model = model
        btn = ttk.Button(self, text= 'Generate', command=self.generate)
        btn.grid(row=0, column=1, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W)  
        self.columnconfigure(0, weight=1)        
        for r,(key, value) in enumerate(self.model.setting['parameters'].items()):
            wg = Widgets.create_widget(self, value)
            wg.grid(row=r+1, column=1, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)
        self.generate()
        self.rowconfigure(9, weight=1)

    def generate(self):
        self.model.generate()
        self.spectrum_plot = RotatedSpectrumPlot(self, self.model.spectrum_data['Ntor'], self.model.spectrum_data['Npol'], self.model.spectrum_data['Amp']  )
        self.spectrum_plot.grid(row=0, column=0, rowspan=12,  padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W)  

from pathlib import Path
import AstraBox.WorkSpace as WorkSpace

class FileSourcePanel(tk.Frame):
    def __init__(self, master, path, load_file_cb = None) -> None:
        super().__init__(master)
        self.spectrum_folder = WorkSpace.get_location_path() / 'spectrum_data'
        print(self.spectrum_folder)
        self.load_file_cb = load_file_cb
        self.path_var = tk.StringVar(master= self, value=path)
        label = tk.Label(master=self, text='Source:')
        label.pack(side = tk.LEFT, padx=2)		
        entry = tk.Entry(self, width=65, textvariable= self.path_var)
        entry.pack(side = tk.LEFT, padx=2)
        btn1 = ttk.Button(self, text= 'Select file', command=self.select_file)
        btn1.pack(side = tk.LEFT, padx=10)   

    def load_file(self):
        if self.load_file_cb:
            self.load_file_cb(self.path_var.get())

    def select_file(self):
        filename = fd.askopenfilename(initialdir= self.spectrum_folder)
        if len(filename) < 1 : return
        fp = Path(filename)
        if fp.is_relative_to(self.spectrum_folder):
            filename = fp.name
        self.path_var.set(filename)
        if self.load_file_cb:
            self.load_file_cb(filename)



class Spectrum1DView(tk.LabelFrame):
    def __init__(self, master, model: SpectrumModel) -> None:
        super().__init__(master, text='Spectrum 1D')        

        #self.header_content = { "title": 'title', "buttons":[('Save', None), ('Delete', None), ('Clone', None)]}
        self.model = model

        self.control_panel = FileSourcePanel(self, self.model.setting['source'], self.on_load_file)
        self.control_panel.grid(row=0, column=0, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W) 
        self.columnconfigure(0, weight=1)        
        #self.rowconfigure(0, weight=1)    
        self.make_plot()
        #wg1 = Widgets.create_widget(self, self.model.setting['parameters']['angle'])
        #wg1.grid(row=1, column=1, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)
        wg2 = Widgets.create_widget(self, self.model.setting['parameters']['spline'])
        wg2.grid(row=1, column=1, padx=5, sticky=tk.N)

        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=0)
        self.rowconfigure(3, weight=1)        

    def on_load_file(self, filename):
        print(filename)
        self.model.setting['source'] = filename
        self.make_plot()

    def make_plot(self):
        self.model.read_spcp1D()
        self.spectrum_plot = SpectrumPlot(self, self.model.spectrum_data['Ntor'], self.model.spectrum_data['Amp']  )
        self.spectrum_plot.grid(row=1, column=0,  rowspan=3, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W) 

class ScatterSpectrumView(tk.LabelFrame):
    def __init__(self, master, model=None) -> None:
        super().__init__(master, text='Scatter Spectrum')        

        #self.header_content = { "title": 'title', "buttons":[('Save', None), ('Delete', None), ('Clone', None)]}
        self.model = model

        self.control_panel = FileSourcePanel(self, self.model.setting['source'], self.on_load_file)
        self.control_panel.grid(row=0, column=0, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W) 
        radio_selector = self.make_radio_selector()
        radio_selector.grid(row=0, column=1, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W) 
        self.columnconfigure(0, weight=1)        
        #self.rowconfigure(0, weight=1)    
        self.make_plot(self.model.setting['source'])

    def on_load_file(self, filepath):
        print(filepath)
        
        if self.make_plot(filepath):
            self.model.setting['source'] = filepath

    def make_plot(self, filepath):
        head, filename = os.path.split(filepath)
        return self.make_scatter_plot3D(filepath)

    def make_scatter_plot3D(self, filepath):
        self.model.read_scatter(filepath)
            
        if self.model.spectrum_data == None:
            label = ttk.Label(self, text="Spectrum None", width=20)
            label.grid(row=1, column=0, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W)       
            return False
        else:
            self.spectrum_plot = ScatterPlot2D3D(self, self.model.spectrum_data)
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
        self.spectrum_plot = ScatterPlot2D3D(self, self.model.spectrum_data)
        self.spectrum_plot.grid(row=1, column=0, columnspan= 2, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W)  
    def select_View3D(self):
        self.spectrum_plot = ScatterPlot3D(self, self.model.spectrum_data)
        self.spectrum_plot.grid(row=1, column=0, columnspan= 2, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W)   
          

class Spectrum2DView(tk.LabelFrame):
    def __init__(self, master, model=None) -> None:
        super().__init__(master, text='Spectrum 2D')        

        #self.header_content = { "title": 'title', "buttons":[('Save', None), ('Delete', None), ('Clone', None)]}
        self.model = model

        self.control_panel = FileSourcePanel(self, self.model.setting['source'], self.on_load_file)
        self.control_panel.grid(row=0, column=0, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W) 
        self.columnconfigure(0, weight=1)        
        #self.rowconfigure(0, weight=1)    
        self.make_plot(self.model.setting['source'])

    def on_load_file(self, filepath):
        print(filepath)
        
        if self.make_plot(filepath):
            self.model.setting['source'] = filepath

    def make_plot(self, filepath):
        #head, filename = os.path.split(filepath)
        return self.make_plot2D(filepath)

    def make_plot2D(self, filepath):
        self.model.read_spcp2D(filepath)
            
        if self.model.spectrum_data == None:
            label = ttk.Label(self, text="Spectrum None", width=20)
            label.grid(row=1, column=0, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W)       
            return False
        else:
            self.spectrum_plot = Plot2DArray(self, self.model.spectrum_data)
            self.spectrum_plot.grid(row=1, column=0, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W)  
            return True
        #self.model.read_spcp1D()
        #self.spectrum_plot = SpectrumPlot(self, self.model.spectrum_data['Ntor'], self.model.spectrum_data['Amp']  )
        #self.spectrum_plot.grid(row=1, column=0, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W) 

