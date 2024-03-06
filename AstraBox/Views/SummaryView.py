import tkinter as tk
import tkinter.ttk as ttk
import pandas as pd

from tkinter.scrolledtext import ScrolledText
from AstraBox.Views.HeaderPanel import HeaderPanel
import AstraBox.Models.ModelFactory as ModelFactory
import AstraBox.Models.RootModel as RootModel
import AstraBox.WorkSpace as WorkSpace
from AstraBox.Models.RaceModel import RaceModel



class SummaryView(ttk.Frame):
    def __init__(self, master, model: RaceModel) -> None:
        super().__init__(master)        
        title = f"{model.name}"

        self.model = model

        self.text_box = ScrolledText(self, wrap="none")
        self.text_box.grid(row=2, column=0, columnspan=5, padx=10, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)
        self.text_box.insert(tk.END, f'Summary for {model.name}:\n')
        info = f"Exp: {model.data['ExpModel']['name']} Equ::{model.data['EquModel']['name']}\n"
        self.text_box.insert(tk.END, info)

        self.text_box.insert(tk.END, 'Driver current:\n')
        self.text_box.insert(tk.END, self.get_current())

        self.columnconfigure(0, weight=1)        
        #self.rowconfigure(0, weight=1)            
        self.rowconfigure(2, weight=1)            
        #self.InitUI(model)

    def get_current(self):
        df = self.model.get_driven_current()
        print(df)
        #pd.set_option('display.max_rows', 5)
        if type(df) is str:
            return df
        else:
            return df.to_string(max_rows = 5) 
        #return df.head(3).to_string() + '\n' + df.tail(3).to_string()