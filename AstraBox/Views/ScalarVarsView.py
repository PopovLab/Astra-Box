import tkinter as tk
import tkinter.ttk as ttk

class ScalarVarsView(ttk.Frame):
    def __init__(self, master, model) -> None:
        super().__init__(master)        
        title = f"{model.name}"
        self.model = model