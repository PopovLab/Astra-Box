import tkinter as tk
import tkinter.ttk as ttk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from AstraBox.ToolBox.VerticalNavigationToolbar import VerticalNavigationToolbar2Tk

from AstraBox.Models.ExpModel import ExpModel, Experiment

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

class ScalarPlot(ttk.Frame):
    def __init__(self, master, time_series) -> None:
        super().__init__(master)  
        self.fig = plt.figure(figsize=(7, 5), dpi=100)        
        #self.fig.suptitle(f'Astra time series. ')
        
        
        self.ax1 = self.fig.subplots(1, 1)
        self.canvas = FigureCanvasTkAgg(self.fig, self)   
        self.show_series(time_series)

        self.canvas.get_tk_widget().grid(row=0, column=1, rowspan=2)
        tb = VerticalNavigationToolbar2Tk(self.canvas, self)
        tb.update()
        tb.grid(row=0, column=0, sticky=tk.N)        

        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

    def show_series(self, time_series):
        self.ax1.clear()
        for key, serie in time_series.items():
            self.ax1.plot(serie['time'], serie['values'], label= key)
        self.ax1.legend(loc='upper right')
        self.canvas.draw()

    def destroy(self):
        print("ScalarPlot destroy")
        if self.fig:
            plt.close(self.fig)
        super().destroy()       

class ScalarVarsView(TabViewBasic):
    def __init__(self, master, model: ExpModel) -> None:
        super().__init__(master, model)        
        title = f"{model.name}"
        self.visible_series = {}
        self.model = model
        self.scalar_plot = None 

    def init_ui(self):
        print('init ScalarVarsView')
        exp = self.model.get_experiment()
        sheet = self.make_sheet(exp.scalars)
        sheet.pack(pady= 5)

    def make_sheet(self, vars: dict):
        frame = tk.Frame(self)
        col_num = 5
        column = 0
        row = 0
        for key, v in vars.items():
            print(key, row, column)
            if type(v) == list:
                text = f'{key:7}: list[{len(v)}]'
            else:
                text = f'{key:7}: {v}'
            e = tk.Entry(frame, relief=tk.GROOVE)
            e.grid(row= row, column= column, sticky=tk.NSEW)            
            e.insert(tk.END, text)
            e.value_key = key
            e.saved_bg= e['bg']
            e.bind("<1>", self.handle_click)
            column = column + 1
            if column>= col_num:
                row = row + 1
                column = 0
        return frame

    def handle_click(self, event):
        print(event.widget.value_key)

        exp = self.model.get_experiment()
        var = exp.scalars[event.widget.value_key]
        if type(var) is not list:
            return
        
        bg = event.widget['bg']
        if event.widget.saved_bg == bg:
           event.widget.configure(bg="deepskyblue")
        else:
            event.widget.configure(bg=event.widget.saved_bg)


        if event.widget.value_key in self.visible_series.keys():
            del self.visible_series[event.widget.value_key]
        else:
            time = [t for t, _ in var]
            value =[v for t, v in var]
            self.visible_series[event.widget.value_key] = {'time': time,  "values": value}
        if self.scalar_plot is None:
            self.scalar_plot = ScalarPlot(self, self.visible_series)
            self.scalar_plot.pack(pady= 5)
        else:
            self.scalar_plot.show_series(self.visible_series)