import tkinter as tk
import tkinter.ttk as ttk
from AstraBox.Models.ExpModel import Experiment

class TabViewBasic(ttk.Frame):
    """Базовый класс для вкладок, для перехвата события видимости, что бы потом инициализировать вкладку"""

    def __init__(self, master, model) -> None:
        super().__init__(master)  
        self.race_model = model

        self.first_time = True
        self.bind('<Visibility>', self.visibilityChanged)
    
    def visibilityChanged(self, event):
        if self.first_time:
            self.first_time = False
            self.init_ui()

    def init_ui(self):
        print('init TabViewBasic')
        pass

class ScalarVarsView(TabViewBasic):
    def __init__(self, master, model) -> None:
        super().__init__(master, model)        
        title = f"{model.name}"
        self.model = model


    def init_ui(self):
        print('init ScalarVarsView')
        exp = self.model.get_experiment()
        sheet = self.make_sheet(exp)
        sheet.pack()

    def make_sheet(self, exp: Experiment):
        frame = tk.Frame(self)
        scalar_list = []
        key_list = list(exp.scalars.keys())
        for key, v in exp.scalars.items():
            if type(v) == list:
                scalar_list.append(f'{key:7}: list[{len(v)}]')
            else:
                scalar_list.append(f'{key:7}: {v}')
        sl = len(scalar_list)
        rows = []
        for i in range(5):
            cols = []
            for j in range(4):
                e = tk.Entry(frame, relief=tk.GROOVE)
                e.grid(row=i, column=j, sticky=tk.NSEW)
                index = i*4 + j
                if index<sl:
                    s =  scalar_list[index]
                    e.insert(tk.END, s)
                    e.value_key = key_list[index]
                    e.bind("<1>", self.handle_click)
                
                #e.insert(tk.END, '%d.%d' % (i, j))
                cols.append(e)
            rows.append(cols)
        return frame

    def handle_click(self, event):
        print(event.widget.value_key)