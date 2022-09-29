import imp
import os
import tkinter as tk
import tkinter.messagebox as messagebox
from AstraBox.Views.RackFrame import RackFrame
from AstraBox.Views.ContentFrame import ContentFrame
from AstraBox.Storage import Storage
from AstraBox.Controller import Controller
import AstraBox.Models.ModelFactory as ModelFactory
class App:
    def __init__(self, root):
        root.title("ASTRA Box")
        root.minsize(1000, 550)


        abspath = os.path.abspath('data')
        if not os.path.exists(abspath):
            os.mkdir(abspath)
        self.base_folder = abspath
        
        store = Storage()
        store.open(abspath)
        self.scan_folders()
        # first paned window
        w1 = tk.PanedWindow( background='#C0DCF3')  
        w1.pack(fill=tk.BOTH, expand=1) 

        # second paned window
        w2 = tk.PanedWindow(w1, orient=tk.VERTICAL)  
        w1.add(w2)  

        rack_frame = RackFrame(w2)
        w2.add(rack_frame)

        self.main_layout = ContentFrame(w1)
        w1.add(self.main_layout)

        Controller().set_views(rack_frame, self.main_layout)

        root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root = root


    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            #self.controller.destroy()
            #Storage().close()
            self.root.destroy()
            

    def scan_folders(self):
        store = Storage()
        path = os.path.join(store.data_folder, 'exp')
        if os.path.exists(path):
            filenames = next(os.walk(path), (None, None, []))[2]
            for f in filenames:
                if not f in store.exp_store.data:
                    store.exp_store.data[f] = ModelFactory.create_model('exp',f)

        path = os.path.join(store.data_folder, 'equ')
        if os.path.exists(path):
            filenames = next(os.walk(path), (None, None, []))[2]
            for f in filenames:
                if not f in store.equ_store.data:
                    store.equ_store.data[f] = ModelFactory.create_model('equ',f)     

        path = os.path.join(store.data_folder, 'sbr')
        if os.path.exists(path):
            filenames = next(os.walk(path), (None, None, []))[2]
            for f in filenames:
                if not f in store.sbr_store.data:
                    store.sbr_store.data[f] = ModelFactory.create_model('sbr',f)           