import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox
from AstraBox.Window import Windows
import AstraBox.WorkSpace as WorkSpace
import AstraBox.History as History

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

        if work_space_location:
            work_space = WorkSpace.WorkSpace(work_space_location)
            History.add_new(work_space_location)
        else:
            work_space = WorkSpace.WorkSpace()

        window = Windows(self, work_space)

        window.protocol("WM_DELETE_WINDOW", lambda: self._on_window_closed(window))

    def _on_window_closed(self, window):
        """Window close handler"""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            window.save_geometry()
            window.destroy()
            self.destroy()
            

    



