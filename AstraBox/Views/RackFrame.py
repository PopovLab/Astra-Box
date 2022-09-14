import tkinter as tk
import tkinter.ttk as ttk
class RackFrame(ttk.Frame):
    def __init__(self, master) -> None:
        super().__init__(master)
        self.on_select = None

        self.v = tk.StringVar(self, "xxx")  # initialize

        ttk.Separator(self, orient='horizontal').pack(fill='x')

        ttk.Radiobutton(self, text="First button", variable=self.v, value="imped", width=25, command= None,
                            style = 'Toolbutton').pack(expand=0, fill=tk.X)

        ttk.Separator(self, orient='horizontal').pack(fill='x')