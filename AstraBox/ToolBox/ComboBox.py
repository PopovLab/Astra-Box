import tkinter as tk
import tkinter.ttk as ttk

class ComboBox(ttk.Frame):
    on_combo_selected = None
    def combo_selected(self, *args):
        self.selected_value = self.combo.get()
        if self.on_combo_selected:
            self.on_combo_selected()
        
    def set(self, value):
        self.combo.set(value)

    def get(self):
        return self.combo.get()

    def __init__(self, master, title, values, width= 17) -> None:
        super().__init__(master)     
        self.selected_value = None
        label = ttk.Label(self, text=title)
        label.grid(row=0, column=0, sticky=tk.W, pady=4, padx=4)
        self.combo = ttk.Combobox(self, width= width )# command=lambda x=self: self.update(x))  
        self.combo.bind("<<ComboboxSelected>>", self.combo_selected)
        self.combo['values'] =  values  #item['value_items'] #
        #self.combo.set(item['value'])
        #self.combo.current(1)  # установите вариант по умолчанию  
        self.combo.grid(row=0, column=1, sticky=tk.W, pady=4, padx=4)
