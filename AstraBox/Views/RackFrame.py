import tkinter as tk
import tkinter.ttk as ttk
from AstraBox.Views.Explorer import Explorer
from AstraBox.Storage import Storage
from AstraBox.Controller import Controller

class RackFrame(ttk.Frame):
    def __init__(self, master) -> None:
        super().__init__(master)
        self.on_select = None
        self.active_exlorer = None
        self.v = tk.StringVar(self, "xxx")  # initialize

        ttk.Separator(self, orient='horizontal').pack(fill='x')

        self.exp_explorer = Explorer(self, title='Experiments', model_store=Storage().exp_store)
        self.exp_explorer.on_select = self.on_explorer_select
        self.exp_explorer.pack(expand=1, fill=tk.BOTH, padx=(10,0), pady=(5,10))   
             
        self.exp_explorer = Explorer(self, title='Equlibrium', model_store=Storage().equ_store)
        self.exp_explorer.on_select = self.on_explorer_select
        self.exp_explorer.pack(expand=1, fill=tk.BOTH, padx=(10,0), pady=(5,20))                

        ttk.Separator(self, orient='horizontal').pack(fill='x')

        self.exp_explorer = Explorer(self, title='Subroutine', model_store=Storage().sbr_store)
        self.exp_explorer.on_select = self.on_explorer_select
        self.exp_explorer.pack(expand=1, fill=tk.BOTH, padx=(10,0), pady=(5,20))                

        ttk.Separator(self, orient='horizontal').pack(fill='x')

        self.rt_explorer = Explorer(self, title='Ray Tracing Configurations', new_button = True, model_store=Storage().rt_store)
        self.rt_explorer.on_select = self.on_explorer_select
        self.rt_explorer.pack(expand=1, fill=tk.BOTH, padx=(10,0), pady=(5,20))                

        ttk.Separator(self, orient='horizontal').pack(fill='x')

        ttk.Radiobutton(self, text="Run ASTRA", variable=self.v, value="imped", width=25, command= self.show_calc_view,
                            style = 'Toolbutton').pack(expand=0, fill=tk.X)

        ttk.Separator(self, orient='horizontal').pack(fill='x')

        self.race_explorer = Explorer(self, title='Race history', model_store=Storage().race_store)
        self.race_explorer.on_select = self.on_explorer_select
        self.race_explorer.pack(expand=1, fill=tk.BOTH, padx=(10,0), pady=(5,20)) 

    def on_explorer_select(self, explorer, model):
        print(model)
        if self.active_exlorer:
            if self.active_exlorer is not explorer:
                self.active_exlorer.selection_clear()

        self.active_exlorer = explorer

        Controller().show_model(model)

    def show_calc_view(self):
        Controller().show_calc_view()
