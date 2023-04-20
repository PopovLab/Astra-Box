import os
import tkinter as tk
import tkinter.ttk as ttk
from AstraBox.Views.ListView import ListView
import AstraBox.Models.ModelFactory as ModelFactory
import AstraBox.WorkSpace as WorkSpace

class RackFrame(ttk.Frame):
    def __init__(self, master, app) -> None:
        super().__init__(master)
        self.app = app
        self.on_select = None
        self.active_exlorer = None
        self.active_view = None
        self.v = tk.StringVar(self, "xxx")  # initialize

        frame = ttk.Frame(self)
        ttk.Radiobutton(frame, text="Open Workspace", variable=self.v, value="owp", width=20, command= self.open_folder_dialog,
                            style = 'Toolbutton').pack(side = tk.LEFT, expand=0, fill=tk.X)
        ttk.Radiobutton(frame, text="Doc", variable=self.v, value="doc", width=4, command= self.open_doc,
                            style = 'Toolbutton').pack(side = tk.LEFT, expand=0, fill=tk.X)
        frame.pack(expand=0, fill=tk.X)
        
        ttk.Separator(self, orient='horizontal').pack(fill='x')

        ListView(self,'ExpModel', command= self.on_select_item).pack(expand=1, fill=tk.BOTH, padx=(10,0), pady=(5,5))
        ListView(self,'EquModel', command= self.on_select_item).pack(expand=1, fill=tk.BOTH, padx=(10,0), pady=(5,5))
        ListView(self,'SbrModel', command= self.on_select_item).pack(expand=1, fill=tk.BOTH, padx=(10,0), pady=(5,5))
        ListView(self,'RTModel', command= self.on_select_item).pack(expand=1, fill=tk.BOTH, padx=(10,0), pady=(5,10))
 
        ttk.Separator(self, orient='horizontal').pack(fill='x')

        ttk.Radiobutton(self, text="Run ASTRA", variable=self.v, value="imped", width=25, command= self.show_RunAstraView,
                            style = 'Toolbutton').pack(expand=0, fill=tk.X)

        ttk.Separator(self, orient='horizontal').pack(fill='x')

        ListView(self,'RaceModel', command= self.on_select_item).pack(expand=1, fill=tk.BOTH, padx=(10,0), pady=(5,10))

    def on_select_item(self, sender, action):
        self.v.set('xxx')
        if self.active_view:
            if self.active_view is not sender:
                self.active_view.selection_clear()
        self.active_view = sender
        model = ModelFactory.do(action)
        self.app.show_model(model)

    def open_doc(self):
        self.app.open_doc()
        self.v.set('xxx')

    def open_folder_dialog(self):
        dir = tk.filedialog.askdirectory()
        if len(dir)>0:
            self.app.open_work_space(dir)
        self.v.set('xxx')

    def show_RunAstraView(self):
        if self.active_exlorer:
            self.active_exlorer.selection_clear()
            self.active_exlorer = None
        self.app.show_RunAstraView()
