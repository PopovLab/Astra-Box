import tkinter as tk
import tkinter.ttk as ttk
from AstraBox.Views.Explorer import Explorer
from AstraBox.Storage import Storage

class RackFrame(ttk.Frame):
    def __init__(self, master) -> None:
        super().__init__(master)
        self.on_select = None

        self.v = tk.StringVar(self, "xxx")  # initialize

        ttk.Separator(self, orient='horizontal').pack(fill='x')

        ttk.Radiobutton(self, text="First button", variable=self.v, value="imped", width=25, command= None,
                            style = 'Toolbutton').pack(expand=0, fill=tk.X)

        ttk.Separator(self, orient='horizontal').pack(fill='x')

        self.exp_explorer = Explorer(self, title='Experiments', model_store=Storage().exp_store)
        #self.spectrum_explorer.on_select = self.explorer_select
        self.exp_explorer.pack(expand=1, fill=tk.BOTH, padx=(10,0), pady=(5,20))        
        self.exp_explorer = Explorer(self, title='Equlibtium')
        #self.spectrum_explorer.on_select = self.explorer_select
        self.exp_explorer.pack(expand=1, fill=tk.BOTH, padx=(10,0), pady=(5,20))                

        ttk.Separator(self, orient='horizontal').pack(fill='x')

        ttk.Radiobutton(self, text="Calculation button", variable=self.v, value="imped", width=25, command= None,
                            style = 'Toolbutton').pack(expand=0, fill=tk.X)

        ttk.Separator(self, orient='horizontal').pack(fill='x')
