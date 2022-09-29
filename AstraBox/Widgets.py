import ast
import tkinter as tk
import tkinter.ttk as ttk
from turtle import width


def create_widget(frame, item):
    return StringBox(frame, item)  

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
    def callback(self):
        print(self.item['title'])
        #print(self.string_var.get())

    def __init__(self, master, item) -> None:
        super().__init__(master)
        self.item = item
        print(item)
        label = ttk.Label(self, text="item['title']", width=20)
        label.grid(row=0, column=0, sticky=tk.W, pady=8, padx=8)
        self.string_var = tk.StringVar(self, value="item['value']")

 
        self.entry = tk.Entry(self, width=20, textvariable= self.string_var, validate="focusout", validatecommand=self.callback)
        self.entry.bind('<Return>',  (lambda event: self.callback() ))
        self.entry.grid(row=0, column=1, columnspan=1)        

class ListBox(ttk.Frame):
    def __init__(self, master, item) -> None:
        super().__init__(master)
        pass

class IntTextBox(ttk.Frame):
    def __init__(self, master, item) -> None:
        super().__init__(master)
        pass    

class FloatTextBox(ttk.Frame):
    def __init__(self, master, item) -> None:
        super().__init__(master)
        pass  