import tkinter as tk
import tkinter.ttk as ttk

class HeaderPanel(ttk.Frame):
    def __init__(self, master, content: dict) -> None:
        super().__init__(master)
        # border=border, borderwidth, class_, cursor, height, name, padding, relief, style, takefocus, width)
        padx = 5
        frame = ttk.Frame(self)
        label = ttk.Label(frame,  text=content['title'], style="Header.TLabel")
        label.pack(side=tk.LEFT, padx=padx, pady=0)

        for text, command in content['buttons']:
            btn = ttk.Button(frame, text=text, style = 'Toolbutton', command=command)
            btn.pack(side=tk.RIGHT, expand=0, padx=20, pady=0)

        frame.pack(fill='x')
        ttk.Separator(self, orient='horizontal').pack(fill='x')