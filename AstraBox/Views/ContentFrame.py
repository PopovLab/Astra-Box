import tkinter as tk
import tkinter.ttk as ttk
from AstraBox.Views.EmptyView import EmptyView

class ContentFrame(ttk.Frame):
    def __init__(self, master) -> None:
        super().__init__(master)        
        self.content = None
        self.columnconfigure(0, weight=1)        
        self.rowconfigure(0, weight=1)        

    def set_content(self, content):
        #self.label.config(text = content.title)
        if self.content:
            self.content.destroy()
       
        self.content = content
        self.content.grid(row=0, column=0, padx=10, sticky=tk.N + tk.S + tk.E + tk.W)     

    def show_empty_view(self):
        self.set_content(EmptyView(self))