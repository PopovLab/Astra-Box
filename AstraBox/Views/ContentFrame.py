import tkinter as tk
import tkinter.ttk as ttk
from AstraBox.Pages.EmptyPage import EmptyPage
from AstraBox.Pages.ReadMePage import ReadMePage

class ContentFrame(ttk.Frame):
    def __init__(self, master) -> None:
        super().__init__(master)        
        self.content = None
        self.columnconfigure(0, weight=1)        
        self.rowconfigure(0, weight=1)        
        self.show_readme()

    def set_content(self, content):
        #self.label.config(text = content.title)
        if self.content:
            self.content.destroy()
       
        self.content = content
        self.content.grid(row=0, column=0, padx=0, sticky=tk.N + tk.S + tk.E + tk.W)     

    def show_empty_view(self):
        self.set_content(EmptyPage(self))

    def show_readme(self):
        self.set_content(ReadMePage(self))        