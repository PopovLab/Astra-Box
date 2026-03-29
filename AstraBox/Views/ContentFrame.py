import tkinter as tk
import tkinter.ttk as ttk
from AstraBox.Pages.EmptyPage import EmptyPage
from AstraBox.Pages.ReadMePage import ReadMePage
from AstraBox.Pages.RunAstraPage import RunAstraPage

class ContentFrame(ttk.Frame):
    def __init__(self, master) -> None:
        super().__init__(master)        
        self._content = None

    def show_page(self, content):
        if self._content:
            self._content.pack_forget()
            if not isinstance(self._content, RunAstraPage):
                self._content.destroy()            
        self._content = content
        self._content.pack(fill="both", expand=True)

    def show_empty_view(self):
        self.show_page(EmptyPage(self))

    def show_readme(self):
        self.show_page(ReadMePage(self))        