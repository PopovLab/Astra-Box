import tkinter as tk
import tkinter.ttk as ttk
from AstraBox.Pages.EmptyPage import EmptyPage
from AstraBox.Pages.ReadMePage import ReadMePage

class ContentFrame(ttk.Frame):
    def __init__(self, master) -> None:
        super().__init__(master)        
        self.content = None

    def show_page(self, content):
        if self.content:
            self.content.destroy()
        self.content = content
        self.content.pack(fill="both", expand=True)

    def show_empty_view(self):
        self.show_page(EmptyPage(self))

    def show_readme(self):
        self.show_page(ReadMePage(self))        