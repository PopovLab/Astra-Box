import tkinter as tk
import tkinter.ttk as ttk
from AstraBox.Views.HeaderPanel import HeaderPanel
from AstraBox.Storage import Storage

class ComboBox(ttk.Frame):
    def combo_selected(self, *args):
        self.selected_value = self.combo.get()
        
    def __init__(self, master, title, values) -> None:
        super().__init__(master)     
        self.selected_value = None
        label = ttk.Label(self, text=title, width=20)
        label.grid(row=0, column=0, sticky=tk.W, pady=4, padx=8)
        self.combo = ttk.Combobox(self, width=17 )# command=lambda x=self: self.update(x))  
        self.combo.bind("<<ComboboxSelected>>", self.combo_selected)
        self.combo['values'] =  values  #item['value_items'] #
        #self.combo.set(item['value'])
        #self.combo.current(1)  # установите вариант по умолчанию  
        self.combo.grid(row=1, column=0)


class CalculationView(ttk.Frame):
    def __init__(self, master) -> None:
        super().__init__(master)        
        self.header_content =  { "title": "Calculation", "buttons":[('Run calculation', self.start), ('Terminate', self.terminate), ('Test', None)]}
        
        self.hp = HeaderPanel(self, self.header_content)
        self.hp.grid(row=0, column=0, columnspan=5, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)
        self.columnconfigure(4, weight=1)        
        #self.rowconfigure(0, weight=1)    
        self.exp_combo = ComboBox(self, 'Experiments', Storage().exp_store.get_keys_list())
        self.exp_combo.grid(row=1, column=0, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)
        self.equ_combo = ComboBox(self, 'Equlibrium', Storage().equ_store.get_keys_list())
        self.equ_combo.grid(row=1, column=1, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)        
        self.rt_combo = ComboBox(self, 'RT configuration', Storage().rt_store.get_keys_list())
        self.rt_combo.grid(row=1, column=2, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)

    def start(self):
        pass

    def terminate(self):
        pass