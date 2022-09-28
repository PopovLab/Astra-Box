import tkinter as tk
import tkinter.ttk as ttk
from AstraBox.Views.HeaderPanel import HeaderPanel

class TextView(ttk.Frame):
    def __init__(self, master, model) -> None:
        super().__init__(master)        
        #self.title = 'ImpedModelView'
        title = f"Text View {model.name}"
        self.header_content = { "title": title, "buttons":[('Save', None), ('Delete', None), ('Clone', None)]}
        self.model = model
        self.hp = HeaderPanel(self, self.header_content)
        self.hp.grid(row=0, column=0, columnspan=5, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)
        self.text = tk.Text(self, bg = "light cyan", wrap="none")
        self.text.grid(row=1, column=0, columnspan=5, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)
        self.text.insert(tk.END, model.get_text())


        self.columnconfigure(0, weight=1)        
        #self.rowconfigure(0, weight=1)            
        self.rowconfigure(1, weight=1)            
        #self.InitUI(model)