import tkinter as tk
import tkinter.messagebox as messagebox
from AstraBox.Views.RackFrame import RackFrame
from AstraBox.Views.ContentFrame import ContentFrame

class App:
    def __init__(self, root):
        root.title("ASTRA Box")
        root.minsize(800, 450)

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

        root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root = root


    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            #self.controller.destroy()
            #Storage().close()
            self.root.destroy()
            