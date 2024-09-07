import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox

import AstraBox.Models.RootModel as RootModel
from AstraBox.Models.SpectrumModel import SpectrumModel
from AstraBox.Models.RTModel import RTModel
from AstraBox.Views.HeaderPanel import HeaderPanel
import AstraBox.Widgets as Widgets
from AstraBox.Views.FRTCView import FRTCView
import AstraBox.Models.ModelFactory as ModelFactory
import AstraBox.WorkSpace as WorkSpace




class FRTCPage(ttk.Frame):
    def __init__(self, master, folder_item) -> None:
        super().__init__(master)        
        self.folder_item = folder_item
        self.model = ModelFactory.load(folder_item)
        title = f"FRTC: {self.model.name}"
        self.header_content = { "title": title, "buttons":[('Save', self.save_model), ('Delete', self.delete_model), ('Clone', self.clone_model)]}
        self.hp = HeaderPanel(self, self.header_content)
        self.hp.grid(row=0, column=0, columnspan=5, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)

        self.columnconfigure(0, weight=0)        
        self.columnconfigure(1, weight=1)         

        self.view = FRTCView(self, self.model)
        self.view.grid(row=1, column=0,columnspan=3, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)
        

    def clone_model(self):
        name = self.var_name.get()
        self.var_name.set(f'{name}_clone_{RootModel.get_uuid_id()[0:4]}')
        self.model.name = self.var_name.get()
        self.model.setting['Comments']['value'] = self.comment_text.get("1.0",tk.END)
        self.model.path = self.model.path.with_stem(self.model.name)
        self.model.save_to_json()
        WorkSpace.refresh_folder('RTModel') 
        
    def save_model(self):
        self.view.update_model()
        self.folder_item.save_model(self.model)

    
    def delete_model(self):
        if self.folder_item.remove():
            self.master.show_empty_view()