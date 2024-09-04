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

            self.notebook = ttk.Notebook(self)
            self.notebook.grid(row=4, column=0,columnspan=3, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)
            for sec in model.get_sections():
                print('-----------------------------')
                print(sec.title)
                #frame = ttk.Frame(self.notebook)
                frame = SectionView(self.notebook, sec) 
                self.notebook.add(frame, text=sec.title, underline=0, sticky=tk.NE + tk.SW)
            
        

                #for row, (_, item) in enumerate(value.items()):
                #    wg = Widgets.create_widget(frame, item)
                #    wg.grid(row=row%ROW_MAX, column=row//ROW_MAX, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)

if __name__ == '__main__':
    frtc = FRTCModel()
    #save_rtp(frtc, 'test_frtc_model.txt')
    root = tk.Tk() 

    root.geometry ("700x600") 
    view = FRTCView(root, frtc)
    view.pack()
    root.mainloop()

    o = frtc.options

    print(o.xyz)
    o.zyx = 31.415
    print(o.zyx)
    #print(pp.zyx.title)
    print(o.model_json_schema())
    for sec in frtc.get_sections():
        print('-----------------------------')
        print(sec)
        schema= sec.model_json_schema()['properties']
        #print(schema)
        for name, value in sec:
            s = schema[name]
            print(f' - {s["title"]}: {value}  -- {s.get("description")}')
            print()
