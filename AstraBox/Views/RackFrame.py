import os
import tkinter as tk
import tkinter.ttk as ttk
from AstraBox.Views.ListView  import ListView
from AstraBox.Views.TableView import TableView 


def construct(master, app):
    rf = RackFrame(master, app)
    for f in app.work_space.folders:
        if f.tag == 'top':
            ListView(rf, f, command= rf.on_select_item).pack(expand=1, fill=tk.BOTH, padx=(10,0), pady=(5,5))

    ttk.Separator(rf, orient='horizontal').pack(fill='x')

    ttk.Radiobutton(rf, text="Run ASTRA", variable= rf.v, value="imped", width=25, 
                    command= rf.show_RunAstraPage,
                    style = 'Toolbutton').pack(expand=0, fill=tk.X)

    ttk.Separator(rf, orient='horizontal').pack(fill='x')
    for f in app.work_space.folders:
        if f.tag == 'bottom':
            TableView(rf, f, height= 8, command= rf.on_select_item).pack(expand=1, fill=tk.BOTH, padx=(10,0), pady=(5,10))
    return rf

class RackFrame(ttk.Frame):
    def __init__(self, master, app) -> None:
        super().__init__(master)
        self.app = app
        self.on_select = None
        self.active_view = None
        self.v = tk.StringVar(self, "xxx")  # initialize

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
