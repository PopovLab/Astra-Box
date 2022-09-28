from AstraBox.Models.ExpModel import ExpModel
from AstraBox.Models.EquModel import EquModel
from AstraBox.Models.SbrModel import SbrModel
from AstraBox.Models.RTModel import RTModel

def create_model(model_type, model_name):
    match model_type:
        case 'exp':
            print(f'create rt - {model_name}')
            model = ExpModel(model_name)        
        case 'equ':
            print(f'create rt - {model_name}')
            model = EquModel(model_name)        
        case 'sbr':
            print(f'create rt - {model_name}')
            model = SbrModel(model_name)        
        case 'rt':
            print(f'create rt - {model_name}')
            model = RTModel(model_name)
        case _:
            print("Это другое")
            model = None
    return model