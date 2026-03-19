import importlib
import os
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox
from functools import partial
from AstraBox.Pages.FRTCPage import FRTCPage
from AstraBox.Pages.SpectrumPage import SpectrumPage
from AstraBox.Views.FRTCView import FRTCView
import AstraBox.Views.RackFrame as RackFrame
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

def clone_model(model):
    model = ModelFactory.clone_model(model)
    WorkSpace.save_model(model)
    print(type(model).__name__)
    WorkSpace.refresh_folder(type(model).__name__) 

geo_file = "data/geo.ini"

def load_geometry():
    try:
        # get geometry from file 
        f = open(geo_file,'r')
        geo =f.read()
        f.close()
    except:
        print ('error reading geo-file')    
        geo = None
    return geo

def save_geometry(geo):
        # save current geometry to the file 
        try:
            with open(geo_file, 'w') as f:
                f.write(geo)
                print('save geo')
                f.close()
        except:
            print('file error')    

import tomllib
def get_version(pk_name):
    try:
        with open("pyproject.toml", "rb") as f:
            pyproject = tomllib.load(f)
        version = pyproject["project"]["version"]
    except Exception as e:
        version = importlib.metadata.version(pk_name)
    return version

from tkinter import filedialog

class Windows(tk.Toplevel):
    def __init__(self, master) -> None:
        super().__init__(master)
        self.app = master
        self.title("ASTRA Box")
        self.minsize(1024, 600)        
        geo = load_geometry()
        if geo:
            self.geometry(geo)
        self.work_space = None
        self.content_frame = None
        main_menu = self.create_main_menu(self)
        self.config(menu= main_menu)        

    def create_main_menu(self, win):
        new_menu = tk.Menu(win, tearoff=0)
        new_menu.add_command(label='FRTC Configurations', command=self.create_FRTC_configuration)
        new_menu.add_command(label='Experiments', state='disabled')
        new_menu.add_command(label='Equlibrium', state='disabled')
        new_menu.add_command(label='gauss spectrum', command= lambda: self.create_spectrum('gauss'))
        new_menu.add_command(label='spectrum 1D', command= lambda: self.create_spectrum('spectrum_1D'))
        new_menu.add_command(label='spectrum 2D', command= lambda: self.create_spectrum('spectrum_2D'))
        new_menu.add_command(label='scatter spectrum', command= lambda: self.create_spectrum('scatter_spectrum'))

        file_menu = tk.Menu(tearoff=0)
        file_menu.add_cascade(label="New", menu=new_menu)
        file_menu.add_command(label="Open Workspace", command= self.open_work_space_dialog)
        file_menu.add_cascade(label="Open Recent", menu= self.create_open_recent_menu)
        file_menu.add_command(label="Save", state='disabled')
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command= self.app._on_window_closed)

        main_menu = tk.Menu()
        main_menu.add_cascade(label="File", menu=file_menu)
        main_menu.add_cascade(label="Help", command=self.open_doc)
        main_menu.add_cascade(label="About", command=self.show_about)
        return main_menu     

    def create_FRTC_configuration(self):
        model = ModelFactory.create_model('FRTCModel')
        WorkSpace.save_model(model)
        WorkSpace.refresh_folder('FRTCModel') 

    def create_spectrum(self, spectrum_type:str):
        print('create_gauss_spectrum')
        model = ModelFactory.create_spectrum_model(spectrum_type)
        WorkSpace.save_model(model)
        WorkSpace.refresh_folder('SpectrumModel') 

    def create_open_recent_menu(self, win):
        menu = tk.Menu(tearoff=0)
        hi = History.get_list()
        for item in reversed(hi):
            menu.add_command(label= item, command= lambda item=item:  self.open_work_space(win, item))
        return menu
    
    def open_doc(self):
        wp = WorkSpace.get_location_path()
        doc_path = wp.joinpath('doc/html/publish/index.html')
        if doc_path.exists():
            os.system(f'start {doc_path.as_posix()}/')            
        else:
            if messagebox.askokcancel("Doc problems", "Can't find local documentation. Do you want to open it online?"):
                url = 'https://temper8.github.io/FRTC_v2'
                os.startfile(url)

    def show_RunAstraPage(self):
        print('show_calc_view')
        view = RunAstraPage(self.content_frame)  
        self.content_frame.set_content(view)

    def show_about(self):
        my_version = get_version('AstraBox')
        messagebox.showinfo("Astra Box", f"version {my_version}")    

    def show_FolderItem(self, folder_item):
        
        match folder_item.model_kind:
            case 'ExpModel':
                model = ModelFactory.load(folder_item)
                page = ExpPage(self.content_frame, folder_item, model)                     
            case 'EquModel':
                model = ModelFactory.load(folder_item)
                page = TextPage(self.content_frame, folder_item, model)     
            case 'SbrModel':
                model = ModelFactory.load(folder_item)
                page = TextPage(self.content_frame, folder_item, model)                   
            case 'RaceModel':
                #model = RaceModel(path= view_item.path )  
                page = RacePage(self.content_frame, folder_item)                 
            case 'RTModel':
                model = ModelFactory.load(folder_item)
                page = RayTracingPage(self.content_frame, folder_item, model)                  
            case 'FRTCModel':
                #model = ModelFactory.load(folder_item)
                page = FRTCPage(self.content_frame, folder_item)                    
            case 'SpectrumModel':
                #model = ModelFactory.load(folder_item)
                page = SpectrumPage(self.content_frame, folder_item)                    
            case _:
                print('create Emptyview')
                page = EmptyPage(self.content_frame)  
        self.content_frame.set_content(page)

    def open_work_space_dialog(self):
        dir = filedialog.askdirectory()
        self.update_idletasks() # An update is needed to avoid freezes.
        print(dir)
        if len(dir)>0:
            self.open_work_space(dir)

    def open_work_space(self, path):
        save_geometry(self.geometry())
        self.destroy()
        self.app.create_window(path)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        work_space_location = History.get_last()  
        self.withdraw()
  
        style = ttk.Style()
        # стиль для кнопок
        # Justify to the left [('Button.label', {'sticky': 'w'})]
        style.layout("TButton", [('Button.button', {'sticky': 'nswe', 'children': [('Button.focus', {'sticky': 'nswe', 'children': [('Button.padding', {'sticky': 'nswe', 'children': [('Button.label',
            {'sticky': 'w'})]})]})]})])

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
                
        self.create_window(work_space_location)
      
    def create_window(self, work_space_location):
        """Creates a new application window."""
        window = Windows(self)

        window.protocol("WM_DELETE_WINDOW", lambda: self._on_window_closed(window))

        if work_space_location:
            window.title(f"ASTRA Box in {work_space_location}")            
            window.work_space= WorkSpace.open(work_space_location)
            History.add_new(work_space_location)
        else:
            window.work_space=  WorkSpace.open()
            
        # first paned window
        main_panel = tk.PanedWindow(window, background='#C0DCF3')  
        main_panel.pack(fill=tk.BOTH, expand=1) 

        # second paned window
        left_panel = tk.PanedWindow(main_panel, orient=tk.VERTICAL)  
        main_panel.add(left_panel)  

        rack_frame = RackFrame.construct(left_panel, window)
        left_panel.add(rack_frame)

        window.content_frame = ContentFrame(main_panel)
        main_panel.add(window.content_frame)



    def _on_window_closed(self, window):
        """Window close handler"""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            save_geometry(window.geometry())
            window.destroy()
            self.destroy()
            

    



