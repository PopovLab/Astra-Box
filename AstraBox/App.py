import tkinter 
import tkinter.messagebox as messagebox

class App:
    def __init__(self, root):
        root.title("ASTRA Box")
        root.minsize(800, 450)

        root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root = root


    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            #self.controller.destroy()
            #Storage().close()
            self.root.destroy()
            