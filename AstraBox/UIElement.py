import ast
import tkinter as tk
import tkinter.ttk as ttk
from turtle import width
from tktooltip import ToolTip

LABEL_WIDTH = 12

def construct(master, value, schema):
    #print(value)
    #print(schema)
    #return StringBox(frame, item)  
    match schema['type']:
        case 'integer':
            ui =  IntegerField(master, value, schema)
        case 'number':
            ui = NumberField(master, value, schema)
    return ui



class IntegerField(ttk.Frame):
    def __init__(self, master, value, schema) -> None:
        super().__init__(master)
        self.value = value
        description = schema.get('description')
        label = ttk.Label(self, text=schema['title'], width=LABEL_WIDTH)
        label.grid(row=0, column=0, sticky=tk.W, pady=4, padx=4)
        if description: 
            ToolTip(label, description, delay=0.1)

        self.tk_var = tk.IntVar(self, value= value)
        self.tk_var.trace_add('write', self.update_var)
 
        self.entry = tk.Entry(self, width=20, textvariable= self.tk_var)
        self.entry.grid(row=0, column=1, columnspan=1)        
        if description: 
            ToolTip(self.entry, schema['description'], delay=0.1)

    def update_var(self, var, indx, mode):
        try:
            self.value = self.tk_var.get()
            self.entry.configure({"background": 'white'})
        except Exception :
            self.entry.configure({"background": 'red'})  


class NumberField(ttk.Frame):
    def __init__(self, master, value, schema) -> None:
        super().__init__(master)
        self.value = value
        description = schema.get('description')
        label = ttk.Label(self, text=schema['title'], width=LABEL_WIDTH)
        label.grid(row=0, column=0, sticky=tk.W, pady=4, padx=4)
        if description: 
            ToolTip(label, description, delay=0.1)

        self.tk_var = tk.DoubleVar(self, value=value)
        self.tk_var.trace_add('write', self.update_var)
 
        self.entry = tk.Entry(self, width=20, textvariable= self.tk_var)
        self.entry.grid(row=0, column=1, columnspan=1)        
        if description: 
            ToolTip(self.entry, schema['description'], delay=0.1)

    def update_var(self, var, indx, mode):
        try:
            self.value = self.tk_var.get()
            self.entry.configure({"background": 'white'})
        except Exception :
            self.entry.configure({"background": 'red'})        