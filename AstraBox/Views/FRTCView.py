import pathlib 
import tkinter as tk
import tkinter.ttk as ttk
from AstraBox.Models.FRTCModel import FRTCModel, ParametersSection
import AstraBox.UIElement as UIElement

ROW_MAX = 7 

class SectionView(tk.Frame):
    def __init__(self, master, section:ParametersSection, state:str= 'normal') -> None:
            super().__init__(master)
            self.section = section
            count=0
            schema= section.model_json_schema()['properties']
            UIElement.LABEL_WIDTH = 12
            for name, value in section:
                e = UIElement.construct(self, name, value, schema[name], self.observer, state)
                e.grid(row=count%ROW_MAX, column=count//ROW_MAX, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)
                count = count + 1

    def observer(self, name, value):
        print(f'{name} {value}')
        setattr(self.section, name, value)

class FRTCView(tk.Frame):
    def __init__(self, master, model:FRTCModel, state:str ='normal') -> None:
            super().__init__(master) 
            self.model = model

            self.columnconfigure(0, weight=0)        
            self.columnconfigure(1, weight=1)         

            self.label = ttk.Label(self,  text='Name:')
            self.label.grid(row=0, column=0, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W)
            self.var_name = tk.StringVar(master= self, value=model.name)
            self.name_entry = ttk.Entry(self, textvariable = self.var_name, state= state)
            self.name_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

            self.label = ttk.Label(self,  text='Comment:')
            self.label.grid(row=1, column=0, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)
            self.comment_text = tk.Text(self, height=3,  wrap="none")
            self.comment_text.grid(row=1, column=1, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)
            self.comment_text.insert(tk.END, model.comment)
            if state=='disabled':
                 self.comment_text.configure(state="disabled")
    
            self.notebook = ttk.Notebook(self)
            self.notebook.grid(row=2, column=0, columnspan=3, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)
            for sec in model.get_sections():
                frame = SectionView(self.notebook, sec, state= state) 
                self.notebook.add(frame, text=sec.title, underline=0, sticky=tk.NE + tk.SW)
            
    def update_model(self):
        self.model.name = self.var_name.get()
        self.model.comment = self.comment_text.get("1.0","end-1c")


def save_dump(frtc_dump, fn):
    loc = pathlib.Path(fn)
    with open(loc, "w" , encoding='utf-8') as file:
            file.write(frtc_dump)

frtc_dump_file = 'frtc_dump.json'

if __name__ == '__main__':
    global view
    loc = pathlib.Path(frtc_dump_file)
    if loc.exists():
        with open(loc, encoding='utf-8') as file:
                dump = file.read()
        frtc = FRTCModel.construct(dump)
        print(f'frtc load from {frtc_dump_file}')
    else:
        frtc = FRTCModel()
        print(f'create new frtc')
    #save_rtp(frtc, 'test_frtc_model.txt')
    root = tk.Tk() 
    root.geometry ("700x600") 
    view = FRTCView(root, frtc)
    view.pack()
    btn = tk.Button(master=root, text='Update Model', command= lambda  : view.update_model())
    btn.pack()
    root.mainloop()

    print('save dump')
    save_dump(frtc.get_dump(), frtc_dump_file)
 