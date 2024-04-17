import tkinter as tk
import tkinter.ttk as ttk
from AstraBox.Views.HeaderPanel import HeaderPanel

class EmptyPage(ttk.Frame):
    def __init__(self, master, model=None) -> None:
        super().__init__(master)        
        #self.title = 'ImpedModelView'
        if model:
            title = f"Empty Model Page {model.name}"
        else:
            title = "Empty Page"
        self.header_content = { "title": title, "buttons":[('Save', None), ('Delete', None), ('Clone', None)]}
        #self.model = model
        self.hp = HeaderPanel(self, self.header_content)
        self.hp.grid(row=0, column=0, columnspan=5, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)
        self.columnconfigure(0, weight=1)        
        #self.rowconfigure(0, weight=1)    

        #self.InitUI(model)