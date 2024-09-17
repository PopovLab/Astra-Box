import tkinter as tk
import tkinter.ttk as ttk




class InfoPanel(tk.Frame):
    def __init__(self, master, model) -> None:
        super().__init__(master) #, text= 'Race info')
        if model.version == 'v1':
            info = {
                'Exp:': model.data['ExpModel']['name'],
                'Equ:': model.data['EquModel']['name'],
                
                }
            if 'RTModel' in  model.data.keys():
                info['Ray tracing:'] = model.data['RTModel']['name']
        else: # v2
            info = {
                'Exp:': model.task.exp,
                'Equ:': model.task.equ,
                'FRTC:': model.task.frtc,
                'Spectrum:': model.task.spectrum,
                }            
        for key, value in info.items():
            var = tk.StringVar(master= self, value=value)
            label = tk.Label(master=self, text=key)
            label.pack(side = tk.LEFT, ipadx=10)		
            entry = tk.Entry(self, width=20, textvariable= var, state='disabled')
            entry.pack(side = tk.LEFT)
