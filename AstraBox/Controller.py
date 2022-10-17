from AstraBox.Views.EmptyView import EmptyView
from AstraBox.Views.RTModelView import RTModelView
from AstraBox.Views.TextView import TextView
from AstraBox.Views.RaceView import RaceView
from AstraBox.Views.RunAstraView import RunAstraView

class Controller:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Controller, cls).__new__(cls)
        return cls.instance
        
    def __init__(self) -> None:
        print('Controller.init')
        #self.data = None

    def set_views(self, rack_frame, content_frame) ->None:
        self.rack_frame = rack_frame
        self.content_frame = content_frame

    def show_empty_view(self):
        model_view = EmptyView(self.content_frame)  
        self.content_frame.set_content(model_view)

    def show_model(self, model):
        print(model)
        print(f'show {model.name}')
        match model.model_name:
            case 'RTModel':
                model_view = RTModelView(self.content_frame, model)     
            case 'ExpModel':
                model_view = TextView(self.content_frame, model)                     
            case 'EquModel':
                model_view = TextView(self.content_frame, model)     
            case 'SbrModel':
                model_view = TextView(self.content_frame, model)                   
            case 'RaceModel':
                model_view = RaceView(self.content_frame, model)                 
            case _:
                print('create Emptyview')
                model_view = EmptyView(self.content_frame, model)  
        self.content_frame.set_content(model_view)

    def show_calc_view(self):
        print('show_calc_view')
        calc_view = RunAstraView(self.content_frame)  
        self.content_frame.set_content(calc_view)