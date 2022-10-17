import ast
import tkinter as tk
import tkinter.ttk as ttk
from turtle import width


def create_widget(frame, item):
    #return StringBox(frame, item)  

    match item['type']:
        case 'enum':
            wg =  ComboBox(frame, item)
        case 'logical':
            wg = Checkbox(frame, item)
        case 'text':
            wg =  TextBox(frame, item)           
        case 'string':
            wg = StringBox(frame, item)        
        case  'list':
            wg = ListBox(frame, item)           
        case 'int':
            wg = IntTextBox(frame, item)          
        case _:
            wg = FloatTextBox(frame, item)
    return wg

class ComboBox(ttk.Frame):
    def __init__(self, master, item) -> None:
        super().__init__(master)
        pass

class Checkbox(ttk.Frame):
    def __init__(self, master, item) -> None:
        super().__init__(master)
        pass

class TextBox(ttk.Frame):
    def __init__(self, master, item) -> None:
        super().__init__(master)
        pass        

class StringBox(ttk.Frame):
    def __init__(self, master, item) -> None:
        super().__init__(master)
        self.item = item
        #print(item)
        label = ttk.Label(self, text=item['title'], width=10)
        label.grid(row=0, column=0, sticky=tk.W, pady=4, padx=4)
        self.tk_var = tk.StringVar(self, value=item['value'])
        self.tk_var.trace_add('write', self.update_var)
 
        self.entry = tk.Entry(self, width=20, textvariable= self.tk_var)
        self.entry.grid(row=0, column=1, columnspan=1)        

    def update_var(self, var, indx, mode):
        self.item['value'] = self.tk_var.get()

class ListBox(ttk.Frame):
    def __init__(self, master, item) -> None:
        super().__init__(master)
        pass

class IntTextBox(ttk.Frame):
    def __init__(self, master, item) -> None:
        super().__init__(master)
        self.item = item
        #print(item)
        label = ttk.Label(self, text=item['title'], width=10)
        label.grid(row=0, column=0, sticky=tk.W, pady=4, padx=4)
        self.tk_var = tk.IntVar(self, value=item['value'])
        self.tk_var.trace_add('write', self.update_var)
 
        self.entry = tk.Entry(self, width=20, textvariable= self.tk_var)
        self.entry.grid(row=0, column=1, columnspan=1)        

    def update_var(self, var, indx, mode):
        try:
            self.item['value'] = self.tk_var.get()
            self.entry.configure({"background": 'white'})
        except Exception :
            self.entry.configure({"background": 'red'})  

class FloatTextBox(ttk.Frame):
    def __init__(self, master, item) -> None:
        super().__init__(master)
        self.item = item
        #print(item)
        label = ttk.Label(self, text=item['title'], width=10)
        label.grid(row=0, column=0, sticky=tk.W, pady=4, padx=4)
        self.tk_var = tk.DoubleVar(self, value=item['value'])
        self.tk_var.trace_add('write', self.update_var)
 
        self.entry = tk.Entry(self, width=20, textvariable= self.tk_var)
        self.entry.grid(row=0, column=1, columnspan=1)        

    def callback(self):
        print(self.item['title'])
        #print(self.string_var.get())

    def update_var(self, var, indx, mode):
        try:
            self.item['value'] = self.tk_var.get()
            self.entry.configure({"background": 'white'})
        except Exception :
            self.entry.configure({"background": 'red'})