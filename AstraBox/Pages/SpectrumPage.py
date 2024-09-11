import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox

import AstraBox.Models.RootModel as RootModel
from AstraBox.Models.SpectrumModel_v1 import SpectrumModel_v1
from AstraBox.Models.RTModel import RTModel
from AstraBox.Views.HeaderPanel import HeaderPanel
from AstraBox.Views.SpectrumView import GaussianSpectrumView, ScatterSpectrumView, Spectrum1DView, Spectrum2DView
import AstraBox.Widgets as Widgets
from AstraBox.Views.FRTCView import FRTCView
import AstraBox.Models.ModelFactory as ModelFactory
import AstraBox.WorkSpace as WorkSpace


class SpectrumPage(ttk.Frame):
    def __init__(self, master, folder_item) -> None:
        super().__init__(master)        
        self.folder_item = folder_item
        self.model = ModelFactory.load(folder_item)
        title = f"Spectrum: {self.model.name}"
        self.header_content = { "title": title, "buttons":[('Save', self.save_model), ('Delete', self.delete_model), ('Clone', self.clone_model)]}
        self.hp = HeaderPanel(self, self.header_content)
        self.hp.grid(row=0, column=0, columnspan=5, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)

        self.columnconfigure(0, weight=0)        
        self.columnconfigure(1, weight=1)   

        self.label = ttk.Label(self,  text='Name:')
        self.label.grid(row=1, column=0, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W)
        self.var_name = tk.StringVar(master= self, value=self.model.name)
        self.name_entry = ttk.Entry(self, textvariable = self.var_name)
        self.name_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

        self.label = ttk.Label(self,  text='Comment:')
        self.label.grid(row=2, column=0, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)
        self.comment_text = tk.Text(self, height=3,  wrap="none")
        self.comment_text.grid(row=2, column=1, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)
        self.comment_text.insert(tk.END, self.model.comment)


        match self.model.spectrum.kind:
            case 'gauss_spectrum': 
                self.view = GaussianSpectrumView(self, self.model)
            case 'spectrum_1D': 
                self.view = Spectrum1DView(self, self.model)
            case 'spectrum_2D': 
                self.view = Spectrum2DView(self, self.model)                
            case 'scatter_spectrum': 
                self.view = ScatterSpectrumView(self, self.model)                
            case _: 
                self.view = tk.Frame(self)
        
        self.view.grid(row=3, column=0,columnspan=3, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)
        
                                    
    def update_model(self):
        self.model.name = self.var_name.get()
        self.model.comment = self.comment_text.get("1.0","end-1c")

    def clone_model(self):
        self.update_model()
        name = self.model.name
        #self.model.name = f'{name}_clone_{RootModel.get_uuid_id()[0:4]}'

        WorkSpace.refresh_folder('FRTCModel') 
        
    def save_model(self):
        self.update_model()
        self.folder_item.save_model(self.model)

    
    def delete_model(self):
        if self.folder_item.remove():
            self.master.show_empty_view()        