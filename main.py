import tkinter as tk
from AstraBox.App import App
import AstraBox.Window as Window
if __name__ == '__main__':
    #app = App()
    #app.mainloop()
    
    while Window.new_window:
        w = Window.Window()
        w.mainloop()
