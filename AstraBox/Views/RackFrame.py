import tkinter as tk
import tkinter.ttk as ttk
from AstraBox.Views.Explorer import Explorer
import AstraBox.Models.ModelFactory as ModelFactory

class RackFrame(ttk.Frame):
    def __init__(self, master, app) -> None:
        super().__init__(master)
        self.app = app
        self.on_select = None
        self.active_exlorer = None
        self.v = tk.StringVar(self, "xxx")  # initialize

        ttk.Radiobutton(self, text="Open Workspace", variable=self.v, value="pwf", width=25, command= self.open_folder_dialog,
                            style = 'Toolbutton').pack(expand=0, fill=tk.X)

        ttk.Separator(self, orient='horizontal').pack(fill='x')

        self.exp_explorer = Explorer(self, title='Experiments', data_source='exp')
        self.exp_explorer.on_select_item = self.on_explorer_select_item
        self.exp_explorer.pack(expand=1, fill=tk.BOTH, padx=(10,0), pady=(5,5))

        #ttk.Separator(self, orient='horizontal').pack(fill='x')
             
        self.exp_explorer = Explorer(self, title='Equlibrium', data_source='equ')
        self.exp_explorer.on_select_item = self.on_explorer_select_item
        self.exp_explorer.pack(expand=1, fill=tk.BOTH, padx=(10,0), pady=(5,5))                

        #ttk.Separator(self, orient='horizontal').pack(fill='x')

        self.exp_explorer = Explorer(self, title='Subroutine', data_source='sbr')
        self.exp_explorer.on_select_item = self.on_explorer_select_item
        self.exp_explorer.pack(expand=1, fill=tk.BOTH, padx=(10,0), pady=(5,5))                

        #ttk.Separator(self, orient='horizontal').pack(fill='x')

        self.rt_explorer = Explorer(self, title='Ray Tracing Configurations', new_button = True, data_source='ray_tracing')
        self.rt_explorer.on_select_item = self.on_explorer_select_item
        self.rt_explorer.pack(expand=1, fill=tk.BOTH, padx=(10,0), pady=(5,10))                

        ttk.Separator(self, orient='horizontal').pack(fill='x')

        ttk.Radiobutton(self, text="Run ASTRA", variable=self.v, value="imped", width=25, command= self.show_calc_view,
                            style = 'Toolbutton').pack(expand=0, fill=tk.X)

        ttk.Separator(self, orient='horizontal').pack(fill='x')

        self.race_explorer = Explorer(self, title='Race history', data_source='races', height= 10)
        self.race_explorer.on_select_item = self.on_explorer_select_item
        self.race_explorer.pack(expand=1, fill=tk.BOTH, padx=(10,0), pady=(5,10)) 

    def on_explorer_select_item(self, explorer, item):
        print(item)
        if self.active_exlorer:
            if self.active_exlorer is not explorer:
                self.active_exlorer.selection_clear()
        self.active_exlorer = explorer
        if item == 'new_model':
            model = ModelFactory.create_model('ray_tracing')
        else:
            model = ModelFactory.build(item)
        self.app.show_model(model)


    def open_folder_dialog(self):
        dir = tk.filedialog.askdirectory()
        if len(dir)>0:
            self.app.open_work_space(dir)
        #Controller().open_folder_dialog()

    def show_calc_view(self):
        self.app.show_calc_view()
