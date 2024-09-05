import tkinter as tk
import tkinter.ttk as ttk
from AstraBox.Models.FRTCModel import FRTCModel, ParametersSection
import AstraBox.UIElement as UIElement

ROW_MAX = 7 

class SectionView(tk.Frame):
    def __init__(self, master, section:ParametersSection) -> None:
            super().__init__(master)
            count=0
            schema= section.model_json_schema()['properties']
            for name, value in section:
                e = UIElement.construct(self, value, schema[name])
                e.grid(row=count%ROW_MAX, column=count//ROW_MAX, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)
                count = count + 1


class FRTCView(tk.Frame):
    def __init__(self, master, model:FRTCModel) -> None:
            super().__init__(master) 
            self.model = model

            self.columnconfigure(0, weight=0)        
            self.columnconfigure(1, weight=1)         

            self.label = ttk.Label(self,  text='Name:')
            self.label.grid(row=0, column=0, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W)
            self.var_name = tk.StringVar(master= self, value=model.name)
            self.name_entry = ttk.Entry(self, textvariable = self.var_name)
            self.name_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

            self.label = ttk.Label(self,  text='Comment:')
            self.label.grid(row=1, column=0, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)
            self.comment_text = tk.Text(self, height=3,  wrap="none")
            self.comment_text.grid(row=1, column=1, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)
            self.comment_text.insert(tk.END, model.comment)
    
            self.notebook = ttk.Notebook(self)
            self.notebook.grid(row=2, column=0, columnspan=3, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)
            for sec in model.get_sections():
                frame = SectionView(self.notebook, sec) 
                self.notebook.add(frame, text=sec.title, underline=0, sticky=tk.NE + tk.SW)
            
 
if __name__ == '__main__':
    frtc = FRTCModel()
    #save_rtp(frtc, 'test_frtc_model.txt')
    root = tk.Tk() 

    root.geometry ("700x600") 
    view = FRTCView(root, frtc)
    view.pack()
    root.mainloop()

 