import tkinter as tk
import tkinter.ttk as ttk

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
        pass