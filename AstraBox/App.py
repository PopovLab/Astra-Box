import imp
import os
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox
from AstraBox.Views.RackFrame import RackFrame
from AstraBox.Views.ContentFrame import ContentFrame
from AstraBox.Controller import Controller
import AstraBox.Models.ModelFactory as ModelFactory
import AstraBox.Config as Config
import AstraBox.WorkSpace as WorkSpace

class App:
    def __init__(self, root):
        self.tk_root = root        
        root.title("ASTRA Box")
        root.minsize(1150, 850)

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

        self.main_layout = ContentFrame(w1)
        w1.add(self.main_layout)

        Controller().set_views(rack_frame, self.main_layout)

        root.protocol("WM_DELETE_WINDOW", self.on_closing)


    def open_work_space(self, path):
        WorkSpace.getInstance().open(path)
        self.tk_root.title(f"ASTRA Box in {path}")
        Config.set_current_workspace_dir(path)        

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            #self.controller.destroy()
            #Storage().close()
            self.tk_root.destroy()
            

