import imp
import os
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox
from AstraBox.Views.RackFrame import RackFrame
from AstraBox.Views.ContentFrame import ContentFrame

from AstraBox.Views.EmptyView import EmptyView
from AstraBox.Views.RTModelView import RTModelView
from AstraBox.Views.TextView import TextView
from AstraBox.Views.RaceView import RaceView
from AstraBox.Views.RunAstraView import RunAstraView

import AstraBox.Models.ModelFactory as ModelFactory
import AstraBox.Config as Config
import AstraBox.WorkSpace as WorkSpace

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ASTRA Box")
        self.minsize(1060, 750)

        style = ttk.Style()
        # стиль для кнопок

        style.configure('Toolbutton', foreground='maroon', 
                                backgound = 'red',
                                padding= 8,  #{'padx': 5, 'pady': 10},
                                font=('Helvetica', 12))
        style.configure("Header.TLabel", padding=12, font=('Helvetica', 12))

        abspath = os.path.abspath(Config.get_current_workspace_dir())
        if not os.path.exists(abspath):
            os.mkdir(abspath)
        self.base_folder = abspath
        
        self.open_work_space(abspath)
        # first paned window
        w1 = tk.PanedWindow( background='#C0DCF3')  
        w1.pack(fill=tk.BOTH, expand=1) 

        # second paned window
        w2 = tk.PanedWindow(w1, orient=tk.VERTICAL)  
        w1.add(w2)  

        rack_frame = RackFrame(w2, self)
        w2.add(rack_frame)

        self.content_frame = ContentFrame(w1)
        w1.add(self.content_frame)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)


    def open_work_space(self, path):
        WorkSpace.getInstance().open(path)
        self.title(f"ASTRA Box in {path}")
        Config.set_current_workspace_dir(path)        

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            #self.controller.destroy()
            #Storage().close()
            self.destroy()
            



    def show_model(self, model):
        print(model)
        if model is None:
            return
        print(f'show {model.name}')
        match model.model_name:
            case 'RTModel':
                model_view = RTModelView(self.content_frame, model)     
            case 'ExpModel':
                model_view = TextView(self.content_frame, model)                     
            case 'EquModel':
                model_view = TextView(self.content_frame, model)     
            case 'SbrModel':
                model_view = TextView(self.content_frame, model)                   
            case 'RaceModel':
                model_view = RaceView(self.content_frame, model)                 
            case _:
                print('create Emptyview')
                model_view = EmptyView(self.content_frame, model)  
        self.content_frame.set_content(model_view)

    def show_calc_view(self):
        print('show_calc_view')
        calc_view = RunAstraView(self.content_frame)  
        self.content_frame.set_content(calc_view)