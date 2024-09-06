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
    def __init__(self, master, folder_item, model:RTModel) -> None:
        super().__init__(master)        
        self.folder_item = folder_item
        title = f"FRTC Configuration View {model.name}"
        self.header_content = { "title": title, "buttons":[('Save', self.save_model), ('Delete', self.delete_model), ('Clone', self.clone_model)]}
        self.model = model
        self.hp = HeaderPanel(self, self.header_content)
        self.hp.grid(row=0, column=0, columnspan=5, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)

        self.columnconfigure(0, weight=0)        
        self.columnconfigure(1, weight=1)         

        self.view = FRTCView(self, model)
        self.view.grid(row=1, column=0,columnspan=3, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)
        

        
    def on_change_spectrum_type(self):
        print(self.radio.selected)
        self.spectrum_model.spectrum_type = self.radio.selected
        #self.spectrum_model.check_model()   
        if self.spectrum_view:
            self.spectrum_view.destroy()
        self.spectrum_view = self.make_spectum_view()
        self.spectrum_view.grid(row=6, column=0,columnspan=3, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)  
                
        
    def clone_model(self):
        name = self.var_name.get()
        self.var_name.set(f'{name}_clone_{RootModel.get_uuid_id()[0:4]}')
        self.model.name = self.var_name.get()
        self.model.setting['Comments']['value'] = self.comment_text.get("1.0",tk.END)
        self.model.path = self.model.path.with_stem(self.model.name)
        self.model.save_to_json()
        WorkSpace.refresh_folder('RTModel') 
        
    def save_model(self):
        old_path = self.model.path
        self.model.name = self.var_name.get()
        self.model.setting['Comments']['value'] = self.comment_text.get("1.0","end-1c")
        self.model.path = self.model.path.with_stem(self.model.name)
        self.model.save_to_json()
        if (self.model.path != old_path):
            old_path.unlink(missing_ok = True)
        WorkSpace.refresh_folder('RTModel') 
    
    def delete_model(self):
        if self.folder_item.remove():
            self.master.show_empty_view()