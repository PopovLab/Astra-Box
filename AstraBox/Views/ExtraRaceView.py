from cgitb import enable
import tkinter as tk
import tkinter.ttk as ttk

from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import ( FigureCanvasTkAgg, NavigationToolbar2Tk)

from AstraBox.Views.HeaderPanel import HeaderPanel
import AstraBox.Models.ModelFactory as ModelFactory

class ExtraRaceView(ttk.Frame):
 
    def __init__(self, master, model) -> None:
        super().__init__(master)        
        self.master = master
        title = f"Race: {model.name}"
        self.header_content = { "title": title, "buttons":[('Delete', None), ('new windows', None) ]}
        self.model = model
        self.model.load_model_data()
        self.hp = HeaderPanel(self, self.header_content)
        self.hp.grid(row=0, column=0, columnspan=5, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)
        #self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)      

        self.radial_data_list = model.get_radial_data_list()

        profile = self.get_profile(0)

        btn_frame = ttk.Frame(self)
        for key in profile.keys():
            btn = ttk.Button(btn_frame, text = key, width=5, command=lambda x = key: self.generate(x))
            btn.pack(side = tk.LEFT, ipadx=10)	

        btn_frame.grid(row=1, column=0, columnspan=5, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)


    def get_profile(self, index):
        file = self.radial_data_list[index]
        print(f'{file} {index}')
        return self.model.read_radial_data(file)        

    def generate(self, key):
        print(key)
