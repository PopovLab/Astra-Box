import tkinter as tk
import tkinter.ttk as ttk
import tkinter.ttk as ttk
from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import ( FigureCanvasTkAgg, NavigationToolbar2Tk)


class OptionsBox(tk.Frame):
    def __init__(self, master, options) -> None:
        super().__init__(master)
        self.options = options
        for key, value in options.items():
            var = tk.DoubleVar(master= self, name = key, value=value)
            label = tk.Label(master=self, text=key)
            label.pack(side = tk.LEFT, ipadx=10)		
            entry = tk.Entry(self, width=10, textvariable= var)
            entry.pack(side = tk.LEFT)

    def update(self):
        for key in self.options.keys():
            var = tk.DoubleVar(master= self, name = key)
            self.options[key] = var.get()


class SpectrumView(tk.LabelFrame):
    def __init__(self, master, model=None) -> None:
        super().__init__(master, text='Spectrum View')        

        self.header_content = { "title": 'title', "buttons":[('Save', None), ('Delete', None), ('Clone', None)]}
        self.model = model
        self.label = ttk.Label(self,  text=f'Spectrum View')
        self.label.grid(row=0, column=0, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W)  

        self.options_box = OptionsBox(self, self.model.setting['options'])
        self.options_box.grid(row=0, column=0, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W) 
        btn = ttk.Button(self, text= 'Generate', command=self.generate)
        btn.grid(row=0, column=1, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W)  
        self.columnconfigure(0, weight=1)        
        #self.rowconfigure(0, weight=1)    
        self.generate()

    def generate(self):
        self.options_box.update()
        self.model.generate()
        self.spectrum_plot = SpectrumPlot(self,self.model.spectrum_data['Ntor'], self.model.spectrum_data['Amp']  )
        self.spectrum_plot.grid(row=1, column=0, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W)  



class SpectrumPlot(ttk.Frame):
    def __init__(self, master, X, Y) -> None:
        super().__init__(master)  
        self.fig = plt.figure(figsize=(5, 3), dpi=100)
        self.fig.add_subplot(111).plot(X, Y)
        canvas = FigureCanvasTkAgg(self.fig, self)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=0)
        frame = ttk.Frame(self)
        frame.grid(row=0, column=0, sticky=tk.W)
        toobar = NavigationToolbar2Tk(canvas, frame)
        #tb = VerticalNavigationToolbar2Tk(canvas, frame)
        #canvas.get_tk_widget().grid(row=2, column=0)

    def destroy(self):
        print("SpectrumPlot destroy")
        if self.fig:
            plt.close(self.fig)
        super().destroy()       