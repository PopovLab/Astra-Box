import os
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox
from functools import partial
from AstraBox.Views.RackFrame import RackFrame
from AstraBox.Views.ContentFrame import ContentFrame

from AstraBox.Pages.EmptyPage import EmptyPage
from AstraBox.Pages.RayTracingPage import RayTracingPage
from AstraBox.Views.TextView import TextView
from AstraBox.Pages.ExpPage import ExpPage
from AstraBox.Pages.TextPage import TextPage
from AstraBox.Pages.RacePage import RacePage
from AstraBox.Pages.RunAstraPage import RunAstraPage
from AstraBox.Models.RaceModel import RaceModel

import AstraBox.Models.ModelFactory as ModelFactory
import AstraBox.Config as Config
import AstraBox.WorkSpace as WorkSpace
import AstraBox.History as History

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ASTRA Box")
        self.minsize(1024, 600)

        main_menu = self.create_main_menu()
        self.config(menu= main_menu)

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

        #abspath = os.path.abspath(Config.get_current_workspace_dir())
        #if not os.path.exists(abspath):
        #    os.mkdir(abspath)

        last_ws = History.get_last()
        if last_ws:
            self.base_folder = last_ws
            self.open_work_space(last_ws)
        # first paned window
        w1 = tk.PanedWindow(self, background='#C0DCF3')  
        w1.pack(fill=tk.BOTH, expand=1) 

        # second paned window
        w2 = tk.PanedWindow(w1, orient=tk.VERTICAL)  
        w1.add(w2)  

        rack_frame = RackFrame(w2, self)
        w2.add(rack_frame)

        self.content_frame = ContentFrame(w1)
        w1.add(self.content_frame)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)


    def open_work_space_dialog(self):
        dir = tk.filedialog.askdirectory()
        if len(dir)>0:
            self.open_work_space(dir)
        #self.v.set('xxx')

    def open_work_space(self, path):
        WorkSpace.open(path)
        self.title(f"ASTRA Box in {path}")
        #Config.set_current_workspace_dir(path)        
        History.add_new(path)

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

    def show_RunAstraPage(self):
        print('show_calc_view')
        view = RunAstraPage(self.content_frame)  
        self.content_frame.set_content(view)

    def show_about(self):
        messagebox.showinfo("Astra Box", "version x.y.z")

    def show_ViewItem(self, view_item):
        
        match view_item.model_kind:
            case 'RTModel':
                model = ModelFactory.load(view_item.path)
                page = RayTracingPage(self.content_frame, model)     
            case 'ExpModel':
                model = ModelFactory.load(view_item.path)
                page = ExpPage(self.content_frame, model)                     
            case 'EquModel':
                model = ModelFactory.load(view_item.path)
                page = TextPage(self.content_frame, model)     
            case 'SbrModel':
                model = ModelFactory.load(view_item.path)
                page = TextPage(self.content_frame, model)                   
            case 'RaceModel':
                #model = RaceModel(path= view_item.path )  
                page = RacePage(self.content_frame, view_item)                 
            case _:
                print('create Emptyview')
                page = EmptyPage(self.content_frame)  
        self.content_frame.set_content(page)
    

    def create_RT_configuration(self):
        model = ModelFactory.create_model('RTModel')
        self.show_model(model)

    def open_command(self, arg):
        print('open command', arg)
        self.open_work_space(arg)

    def create_open_recent_menu(self):
        menu = tk.Menu(tearoff=0)
        hi = History.get_list()
        for item in reversed(hi):
            menu.add_command(label=item, command= partial(self.open_command, item))
        return menu

    def create_main_menu(self):
        new_menu = tk.Menu(tearoff=0)
        new_menu.add_command(label='Ray Tracing Configurations', command=self.create_RT_configuration)
        new_menu.add_command(label='Experiments', state='disabled')
        new_menu.add_command(label='Equlibrium', state='disabled')

        file_menu = tk.Menu(tearoff=0)
        file_menu.add_cascade(label="New", menu=new_menu)
        file_menu.add_command(label="Open Workspace", command=self.open_work_space_dialog)
        file_menu.add_cascade(label="Open Recent", menu= self.create_open_recent_menu())
        file_menu.add_command(label="Save", state='disabled')
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing)

        main_menu = tk.Menu()
        main_menu.add_cascade(label="File", menu=file_menu)
        main_menu.add_cascade(label="Help", command=self.open_doc)
        main_menu.add_cascade(label="About", command=self.show_about)
        return main_menu