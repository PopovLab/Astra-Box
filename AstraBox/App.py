import imp
import os
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox
from AstraBox.Views.RackFrame import RackFrame
from AstraBox.Views.ContentFrame import ContentFrame

from AstraBox.Pages.EmptyPage import EmptyPage
from AstraBox.Pages.RayTracingPage import RayTracingPage
from AstraBox.Views.TextView import TextView
from AstraBox.Pages.ExpPage import ExpPage
from AstraBox.Pages.TextPage import TextPage
from AstraBox.Pages.RacePage import RacePage
from AstraBox.Views.RunAstraView import RunAstraView

import AstraBox.Models.ModelFactory as ModelFactory
import AstraBox.Config as Config
import AstraBox.WorkSpace as WorkSpace

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ASTRA Box")
        self.minsize(1080, 750)

        style = ttk.Style()
        # стиль для кнопок

        style.configure('Toolbutton', 
                        foreground= 'black', 
                        backgound= 'red',
                        padding= 9,  #{'padx': 5, 'pady': 10},
                        font=('Helvetica', 12))
        style.configure("Header.TLabel",
                        foreground='navy',
                        backgound = 'red',
                        padding=8,
                        font=('Helvetica', 12))

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
        WorkSpace.open(path)
        self.title(f"ASTRA Box in {path}")
        Config.set_current_workspace_dir(path)        

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            #self.controller.destroy()
            #Storage().close()
            self.destroy()
            
    def open_doc(self):
        wp = WorkSpace.get_location_path()
        doc_path = wp.joinpath('doc/html/publish/index.html')
        if doc_path.exists():
            os.system(f'start {doc_path.as_posix()}/')            
        else:
            if messagebox.askokcancel("Doc problems", "Can't find local documentation. Do you want to open it online?"):
                url = 'https://temper8.github.io/FRTC_v2'
                os.startfile(url)



    def show_model(self, model):
        print(model)
        if model is None:
            return
        print(f'show {model.name}')
        match model.model_kind:
            case 'RTModel':
                page = RayTracingPage(self.content_frame, model)     
            case 'ExpModel':
                page = ExpPage(self.content_frame, model)                     
            case 'EquModel':
                page = TextPage(self.content_frame, model)     
            case 'SbrModel':
                page = TextPage(self.content_frame, model)                   
            case 'RaceModel':
                page = RacePage(self.content_frame, model)                 
            case _:
                print('create Emptyview')
                page = EmptyPage(self.content_frame, model)  
        self.content_frame.set_content(page)

    def show_RunAstraView(self):
        print('show_calc_view')
        view = RunAstraView(self.content_frame)  
        self.content_frame.set_content(view)