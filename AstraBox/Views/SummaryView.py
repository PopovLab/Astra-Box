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
        self.text_box.insert(tk.END, self.get_dc_view())

        self.columnconfigure(0, weight=1)        
        #self.rowconfigure(0, weight=1)            
        self.rowconfigure(2, weight=1)            
        #self.InitUI(model)

    def get_dc_view(self):
        df = self.model.get_driven_current()
        #print(df)
        #pd.set_option('display.max_rows', 5)
        if type(df) is str:
            return df
        else:
            text=  df.to_string(max_rows = 5) + '\n'
            #print(df.iloc[-1])
            try:
                row = df.iloc[-1]
                text+= ' ----- last moment dc ---------\n'
                text+= f"time= {row['Time']}\n"
                text+= f"cup= {row['cup']}  cp={row['cp']}\n"
                text+= f"cum= {row['cum']}  cm={row['cm']}\n"
                text+= f"cup0= {row['cup0']}  cp0= {row['cp0']}\n"
                text+= f"cum0= {row['cum0']}  cm0= {row['cm0']}\n"
                text+= f"sigma driven current, MA= {row['cp0'] + row['cm0']}\n"
                text+= f"driven current, MA= {row['cup'] + row['cum']}\n"
            except  Exception as e:
                text+=  str(e)
            return text