import tkinter as tk
import tkinter.ttk as ttk

class HeaderPanel(ttk.Frame):
    def __init__(self, master, content) -> None:
        super().__init__(master, relief=tk.GROOVE)
        # border=border, borderwidth, class_, cursor, height, name, padding, relief, style, takefocus, width)
        padx = 20
        pady = 5
        label = ttk.Label(self,  text=content['title'], style="Header.TLabel")
        label.pack(side=tk.LEFT, padx=padx, pady=pady)

        for text, command in content['buttons']:
            btn = ttk.Button(self, text=text, style = 'Toolbutton', command=command)
            btn.pack(side=tk.RIGHT, padx=padx, pady=pady)