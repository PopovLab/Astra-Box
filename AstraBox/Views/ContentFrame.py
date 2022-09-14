import tkinter as tk
import tkinter.ttk as ttk

class ContentFrame(ttk.Frame):
    def __init__(self, master) -> None:
        super().__init__(master)        
        self.content = None
        self.columnconfigure(0, weight=1)        
        self.rowconfigure(1, weight=1)        
