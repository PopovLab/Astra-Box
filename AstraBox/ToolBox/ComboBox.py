import tkinter as tk
import tkinter.ttk as ttk

class ComboBox(ttk.Frame):
    def combo_selected(self, *args):
        self.selected_value = self.combo.get()
        
    def set(self, value):
        self.combo.set(value)

    def get(self):
        return self.combo.get()

    def __init__(self, master, title, values) -> None:
        super().__init__(master)     
        self.selected_value = None
        label = ttk.Label(self, text=title)
        label.grid(row=0, column=0, sticky=tk.W, pady=4, padx=4)
        self.combo = ttk.Combobox(self, width=17 )# command=lambda x=self: self.update(x))  
        self.combo.bind("<<ComboboxSelected>>", self.combo_selected)
        self.combo['values'] =  values  #item['value_items'] #
        #self.combo.set(item['value'])
        #self.combo.current(1)  # установите вариант по умолчанию  
        self.combo.grid(row=0, column=1, sticky=tk.W, pady=4, padx=4)
