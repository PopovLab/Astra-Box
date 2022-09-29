import tkinter as tk
import tkinter.ttk as ttk
from AstraBox.Views.HeaderPanel import HeaderPanel
import AstraBox.Widgets as Widgets

class RTModelView(ttk.Frame):
    def __init__(self, master, model) -> None:
        super().__init__(master)        
        #self.title = 'ImpedModelView'
        title = f"RT Configuration View {model.name}"
        self.header_content = { "title": title, "buttons":[('Save', None), ('Delete', None), ('Clone', None)]}
        self.model = model
        self.hp = HeaderPanel(self, self.header_content)
        self.hp.grid(row=0, column=0, columnspan=5, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)
        #self.label = ttk.Label(self,  text='ImpedModelView')
        #self.label.place(relx=0.5, rely=0.46, anchor=tk.CENTER)
        #self.label.grid(row=0, column=0, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)
        self.columnconfigure(0, weight=0)        
        self.columnconfigure(1, weight=1)         
        #self.rowconfigure(0, weight=1)            
        #self.InitUI(model)

        self.label = ttk.Label(self,  text='Name:')
        self.label.grid(row=1, column=0, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W)
        self.var_name = tk.StringVar(master= self, value=self.model.name)
        self.name_entry = ttk.Entry(self, textvariable = self.var_name)
        self.name_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

        self.label = ttk.Label(self,  text='Comment:')
        self.label.grid(row=2, column=0, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)
        self.comment_text = tk.Text(self, height=3,  wrap="none")
        self.comment_text.grid(row=2, column=1, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)
        self.comment_text.insert(tk.END, self.model.setting['Comments']['value'])

        self.notebook = ttk.Notebook(self)
        #self.notebook.pack(side="top", expand=1, fill="both", pady=6, padx=6)
        self.notebook.grid(row=4, column=0,columnspan=3, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)
        
        ROW_MAX = 5 
        for key, value in self.model.setting.items():
            if 'value' in value:
                continue
            frame = ttk.Frame(self.notebook)  
            self.notebook.add(frame, text=key, underline=0, sticky=tk.NE + tk.SW)
            for row, (_, item) in enumerate(value.items()):
                wg = Widgets.create_widget(frame, item)
                wg.grid(row=row%ROW_MAX, column=row//ROW_MAX, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)