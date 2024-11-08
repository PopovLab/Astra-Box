import os
import tkinter as tk
import tkinter.ttk as ttk
from AstraBox.Views.ListView  import ListView
from AstraBox.Views.TableView import TableView 


def construct(master, app):
    return RackFrame(master, app)

class RackFrame(ttk.Frame):
    def __init__(self, master, app) -> None:
        super().__init__(master)
        self.app = app
        self.on_select = None
        self.active_view = None
        self.v = tk.StringVar(self, "xxx")  # initialize
        self.compose_ui()

    def compose_ui(self):
        top = list([f for f in self.app.work_space.folders if f.tag == 'top'])

        for i, f in enumerate(top):
            ListView(self, f, grid_index=i, command= self.on_select_item).grid(row=i, column=0,  sticky=tk.N + tk.S + tk.E + tk.W)

        n = len(top)

        ttk.Separator(self, orient='horizontal').grid(row=n, column=0, pady=(5,1),  sticky=tk.N + tk.S + tk.E + tk.W)

        ttk.Radiobutton(self, text="Run ASTRA", variable= self.v, value="imped", width=25, 
                        command= self.show_RunAstraPage,
                        style = 'Toolbutton').grid(row=n+1, column=0,  sticky=tk.N + tk.S + tk.E + tk.W)

        ttk.Separator(self, orient='horizontal').grid(row=n+2, column=0,  sticky=tk.N + tk.S + tk.E + tk.W)

        for f in self.app.work_space.folders:
            if f.tag == 'bottom':
                TableView(self, f, height= 8, grid_index= n+3, command= self.on_select_item).grid(row=n+3, column=0,  sticky=tk.N + tk.S + tk.E + tk.W)

        for i in range(n):
            self.rowconfigure(i, weight=1)
        self.rowconfigure(n+0, weight=0)            
        self.rowconfigure(n+1, weight=0)
        self.rowconfigure(n+2, weight=0)
        self.rowconfigure(n+3, weight=1)
        self.columnconfigure(0, weight=1)

    def on_select_item(self, sender, action):
        self.v.set('xxx')
        if self.active_view:
            if self.active_view is not sender:
                self.active_view.selection_clear()
        self.active_view = sender
        self.app.show_FolderItem(action['payload'])

    def show_RunAstraPage(self):
        if self.active_view:
            self.v.set('xxx')
            self.active_view.selection_clear()
            self.active_view = None
        self.app.show_RunAstraPage()
