import ast
import tkinter as tk
import tkinter.ttk as ttk
from turtle import width
from tktooltip import ToolTip

LABEL_WIDTH = 12

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
        self.item = item
        #print(item)
        label = ttk.Label(self, text=item['title'], width=LABEL_WIDTH)
        label.grid(row=0, column=0, sticky=tk.W, pady=4, padx=4)
        self.tk_var = tk.IntVar(self, value= item['value'])
        self.tk_var.trace_add('write', self.update_var)
 
        #self.entry = tk.Entry(self, width=20, textvariable= self.tk_var)
        self.entry = ttk.Checkbutton(self, text= item['title'], variable=self.tk_var, width=20)
        self.entry.grid(row=0, column=1, columnspan=1)

    def update_var(self, var, indx, mode):
        match self.tk_var.get():
            case 0:
                self.item['value'] = False
            case 1:
                self.item['value'] = True
            case _:
                self.item['value'] = False

           

class TextBox(ttk.Frame):
    def __init__(self, master, item) -> None:
        super().__init__(master)
        pass        

class StringBox(ttk.Frame):
    def __init__(self, master, item, width=20) -> None:
        super().__init__(master)
        self.item = item
        #print(item)
        label = ttk.Label(self, text=item['title'], width=LABEL_WIDTH)
        label.grid(row=0, column=0, sticky=tk.W, pady=4, padx=4)
        #Hovertip(label, item['description'], hover_delay=100)
        self.tk_var = tk.StringVar(self, value=item['value'])
        self.tk_var.trace_add('write', self.update_var)
 
        self.entry = tk.Entry(self, width= width, textvariable= self.tk_var)
        self.entry.grid(row=0, column=1, columnspan=1)        
        #Hovertip(self.entry, item['description'], hover_delay=100)

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
        label = ttk.Label(self, text=item['title'], width=LABEL_WIDTH)
        label.grid(row=0, column=0, sticky=tk.W, pady=4, padx=4)
        ToolTip(label, item['description'], delay=0.1)
        self.tk_var = tk.IntVar(self, value=item['value'])
        self.tk_var.trace_add('write', self.update_var)
 
        self.entry = tk.Entry(self, width=20, textvariable= self.tk_var)
        self.entry.grid(row=0, column=1, columnspan=1)        
        ToolTip(self.entry, item['description'], delay=0.1)

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
        label = ttk.Label(self, text=item['title'], width=LABEL_WIDTH)
        label.grid(row=0, column=0, sticky=tk.W, pady=4, padx=4)
        ToolTip(label, item['description'], delay=0.1)
        self.tk_var = tk.DoubleVar(self, value=item['value'])
        self.tk_var.trace_add('write', self.update_var)
 
        self.entry = tk.Entry(self, width=20, textvariable= self.tk_var)
        self.entry.grid(row=0, column=1, columnspan=1)        
        ToolTip(self.entry, item['description'], delay=0.1)

    def callback(self):
        print(self.item['title'])
        #print(self.string_var.get())

    def update_var(self, var, indx, mode):
        try:
            self.item['value'] = self.tk_var.get()
            self.entry.configure({"background": 'white'})
        except Exception :
            self.entry.configure({"background": 'red'})