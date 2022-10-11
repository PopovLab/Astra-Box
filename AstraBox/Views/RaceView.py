import tkinter as tk
import tkinter.ttk as ttk

from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import ( FigureCanvasTkAgg, NavigationToolbar2Tk)

from AstraBox.Views.HeaderPanel import HeaderPanel


class RaceView(ttk.Frame):
 
    def __init__(self, master, model) -> None:
        super().__init__(master)        
        #self.title = 'ImpedModelView'
        title = f"Race data View {model.name}"
        self.header_content = { "title": title, "buttons":[('Save', None), ('Delete', None), ('Clone', None)]}
        self.model = model
        self.hp = HeaderPanel(self, self.header_content)
        self.hp.grid(row=0, column=0, columnspan=5, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)
        self.columnconfigure(0, weight=1)        
        #self.rowconfigure(0, weight=1)    

        #self.InitUI(model)

        self.label = ttk.Label(self,  text=f'zip file:{model.race_zip_file}')
        self.label.grid(row=1, column=0, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W)        

        self.radial_data_list = model.get_radial_data_list()

        self.var = tk.IntVar(name = 'index')
        self.var.trace_add('write', lambda var, indx, mode: self.update_var())

        slider = tk.Scale( self, variable = self.var, orient = tk.HORIZONTAL, from_=0, to=len(self.radial_data_list), resolution=1, length = 250 )
        slider.grid(row=2, column=0, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W)       
        self.time_var = tk.StringVar() 
        self.label = tk.Label(master=self, textvariable = self.time_var)
        self.label.grid(row=3, column=0, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W)        
        self.plot = None

    def update_var(self):
        print(self.var.get())	        
        file = self.radial_data_list[self.var.get()]
        print(file)
        profiles = self.model.read_radial_data(file)
        txt = f'Astra radial data Time={profiles["Time"]}'
        self.time_var.set(txt)
        if self.plot:
            self.plot.destroy()
        self.plot = SimplePlot(self, profiles)
        self.plot.grid(row=4, column=0, sticky=tk.W, pady=4, padx=8)           


class SimplePlot(ttk.Frame):
    def __init__(self, master, profiles) -> None:
        super().__init__(master)  
        self.fig, axs = plt.subplots(2, 2, figsize=(7, 6))
        axs[0,0].plot(profiles['a'])
        #axs[0,0].plot(profiles2['a'])    
        axs[0,0].set_title("a")

        axs[1,0].plot(profiles['J'])
        #axs[1,0].plot(profiles2['J'])
        axs[1,0].set_title("J")

        axs[0,1].plot(profiles['E'])
        axs[0,1].set_title("E")
    
        axs[1,1].plot(profiles['Johm'])
        axs[1,1].set_title("Johm")

        canvas = FigureCanvasTkAgg(self.fig, self)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=0)
        frame = ttk.Frame(self)
        frame.grid(row=0, column=0, sticky=tk.W)
        toobar = NavigationToolbar2Tk(canvas, frame)
        #tb = VerticalNavigationToolbar2Tk(canvas, frame)
        #canvas.get_tk_widget().grid(row=2, column=0)

    def destroy(self):
        print("SimplePlot destroy")
        if self.fig:
            plt.close(self.fig)
        super().destroy()   