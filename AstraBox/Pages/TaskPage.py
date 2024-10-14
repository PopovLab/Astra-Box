import tkinter as tk
import tkinter.ttk as ttk

from AstraBox import Task
from AstraBox.Models.RaceModel import RaceModel
from AstraBox.RaceTab.RaceView import RadialDataView, TimeSeriesView


class InfoPanel(tk.Frame):
    def __init__(self, master, task) -> None:
        super().__init__(master) #, text= 'Race info')

        info = {
            'Exp:': task.exp,
            'Equ:': task.equ,
            'FRTC:': task.frtc,
            'Spectrum:': task.spectrum,
            }            
        for key, value in info.items():
            var = tk.StringVar(master= self, value=value)
            label = tk.Label(master=self, text=key)
            label.pack(side = tk.LEFT, ipadx=10)		
            entry = tk.Entry(self, width=20, textvariable= var, state='disabled')
            entry.pack(side = tk.LEFT)



class TaskBook(ttk.Notebook):
    def __init__(self, master, model, task: Task) -> None:
        super().__init__(master)        

        time_series_view = TimeSeriesView(self, model= model)
        self.add(time_series_view, text="Time Series", underline=0, sticky=tk.NE + tk.SW)

        radial_data_view = RadialDataView(self, model= model)
        self.add(radial_data_view, text="Radial Data", underline=0, sticky=tk.NE + tk.SW)

class TaskPage(ttk.Frame):
 
    def __init__(self, master, folder_item, task: Task) -> None:
        super().__init__(master)        
        self.master = master
        self.folder_item = folder_item
        self.model = RaceModel.load(folder_item.path)  
        self.model.sel_task = task
        title = f"Race: {self.model.name}"
        print(title)
        print(self.model.sel_task)
        #self.header_content = { "title": title, "buttons":[('Delete', self.delete_model), ('Open', self.open_new_windows), ('Extra', self.open_extra_race_view) ]}

        ip = InfoPanel(self, self.model.sel_task)
        ip.grid(row=0, column=0, columnspan=5, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

        self.notebook = TaskBook(self, self.model, task)
        self.notebook.grid(row=4, column=0, columnspan=3, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)