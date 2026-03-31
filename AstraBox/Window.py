import importlib
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

from AstraBox import History
from AstraBox.Pages.FRTCPage import FRTCPage
from AstraBox.Pages.SpectrumPage import SpectrumPage
from AstraBox.Views.FRTCView import FRTCView
import AstraBox.Views.RackFrame as RackFrame
from AstraBox.Views.ContentFrame import ContentFrame

from AstraBox.Pages.EmptyPage import EmptyPage
from AstraBox.Pages.RayTracingPage import RayTracingPage
from AstraBox.Pages.ExpPage import ExpPage
from AstraBox.Pages.TextPage import TextPage
from AstraBox.Pages.RacePage import RacePage
from AstraBox.Pages.RunAstraPage import RunAstraPage
import AstraBox.Models.ModelFactory as ModelFactory
from AstraBox.WorkSpace import WorkSpace


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


class Windows(tk.Toplevel):
    def __init__(self, master, work_space: WorkSpace) -> None:
        super().__init__(master)
        self.app = master
        self.work_space = work_space
        #self.title("ASTRA Box")
        self.title(f"ASTRA Box in {work_space.location}")
        self.minsize(1024, 600)        
        geo = load_geometry()
        if geo:
            self.geometry(geo)
        main_menu = self.create_main_menu(self)
        self.config(menu= main_menu)        

        # first paned window
        main_panel = tk.PanedWindow(self, background='#C0DCF3')  
        main_panel.pack(fill=tk.BOTH, expand=1) 

        # second paned window
        left_panel = tk.PanedWindow(main_panel, orient=tk.VERTICAL)  
        main_panel.add(left_panel)  

        self.rack_frame = RackFrame.construct(left_panel, self)
        left_panel.add(self.rack_frame)

        self.content_frame = ContentFrame(main_panel)
        main_panel.add(self.content_frame)
        self.content_frame.show_readme()

    def save_geometry(self):
        save_geometry(self.geometry())
    
    def switch_asta_button_style(self):
        self.rack_frame.switch_asta_button_style()
        
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
        file_menu.add_cascade(label="Open Recent", menu= self.create_open_recent_menu())
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
        self.work_space.save_model(model)
        self.work_space.refresh_folder('FRTCModel') 

    def create_spectrum(self, spectrum_type:str):
        print('create_gauss_spectrum')
        model = ModelFactory.create_spectrum_model(spectrum_type)
        self.work_space.save_model(model)
        self.work_space.refresh_folder('SpectrumModel') 

    def create_open_recent_menu(self):
        menu = tk.Menu(tearoff=0)
        hi = History.get_list()
        for item in reversed(hi):
            menu.add_command(label= item, command= lambda item=item:  self.open_work_space(item))
        return menu
    
    def open_doc(self):
        help_path = self.work_space.get_help_path()
        if help_path:
            os.system(f'start {help_path.as_posix()}/')            
        else:
            if messagebox.askokcancel("Doc problems", "Can't find local documentation. Do you want to open it online?"):
                url = 'https://temper8.github.io/FRTC_v2'
                os.startfile(url)

    def show_RunAstraPage(self):
        print('show RunAstraPage')
        page = RunAstraPage.get_instance(self.content_frame)  
        self.content_frame.show_page(page)

    def show_about(self):
        my_version = get_version('AstraBox')
        messagebox.showinfo("Astra Box", f"version {my_version}")    

    def show_FolderItem(self, folder_item):
        
        match folder_item.model_kind:
            case 'ExpModel':
                page = ExpPage(self.content_frame, folder_item)                     
            case 'EquModel':
                page = TextPage(self.content_frame, folder_item)     
            case 'SbrModel':
                  page = TextPage(self.content_frame, folder_item)                   
            case 'RaceModel':
                page = RacePage(self.content_frame, folder_item)                 
            case 'RTModel':
                model = ModelFactory.load(folder_item)
                page = RayTracingPage(self.content_frame, folder_item, model)                  
            case 'FRTCModel':
                page = FRTCPage(self.content_frame, folder_item)                    
            case 'SpectrumModel':
                page = SpectrumPage(self.content_frame, folder_item)                    
            case _:
                print('create Emptyview')
                page = EmptyPage(self.content_frame)  
        self.content_frame.show_page(page)

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
