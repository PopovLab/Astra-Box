import tkinter as tk
import tkinter.ttk as ttk

class SheetView(tk.Frame):
    def __init__(self, master: tk.Misc | None = None, items = [] , col_num= 4) -> None:
        super().__init__(master )
        num = len(items)
        row_num = num//col_num+1
        print(row_num)
        for i in range(row_num):
            for j in range(col_num):
                e = tk.Entry(self, relief=tk.GROOVE)
                e.grid(row=i, column=j, sticky=tk.NSEW)
                index = i*col_num + j
                if index<num:
                    e.insert(tk.END, items[index])
        