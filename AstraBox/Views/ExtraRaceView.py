#from cgitb import enable
import tkinter as tk
import tkinter.ttk as ttk

import numpy as np

from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from mpl_toolkits.axes_grid1 import make_axes_locatable

from AstraBox.Views.HeaderPanel import HeaderPanel
import AstraBox.Models.ModelFactory as ModelFactory

class ExtraRaceView(ttk.Frame):
 
    def __init__(self, master, model) -> None:
        super().__init__(master)        
        self.master = master
        self.plot = None
        title = f"Race: {model.name}"
        self.header_content = { "title": title, "buttons":[]}
        self.model = model
        self.model.load_model_data()
        self.hp = HeaderPanel(self, self.header_content)
        self.hp.grid(row=0, column=0, columnspan=5, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)
        #self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)      

        self.combo_cmap = ttk.Combobox(self, width=17 )# command=lambda x=self: self.update(x))  
        self.combo_cmap.bind("<<ComboboxSelected>>", self.update_palette)
        self.combo_cmap['values'] = ['viridis', 'gray', 
                                        'plasma', 'inferno', 'magma', 'cividis', 
                                        'twilight', 'twilight_shifted', 'hsv',
                                        'flag', 'prism', 'ocean', 'gist_earth', 'terrain']
        self.combo_cmap.set("viridis")        
        self.combo_cmap.grid(row=1, column=0, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)

        self.radial_data_list = model.get_file_list('RADIAL_DATA')

        profile = self.get_profile(0)

        btn_frame = ttk.Frame(self)
        for key in profile.keys():
            btn = ttk.Button(btn_frame, text = key, width=5, command=lambda x = key: self.generate(x))
            btn.pack(side = tk.LEFT, ipadx=10)	

        btn_frame.grid(row=2, column=0, columnspan=5, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)
        self.row_count = 3

    def get_profile(self, index):
        file = self.radial_data_list[index]
        print(f'{file} {index}')
        return self.model.read_radial_data(file)        

    def update_palette(self, *args):
        if self.selected_key:
            self.make_plot()

    def generate(self, key):
        print(key)
        #z = self.make_test()
        self.selected_key = key
        self.z = self.make_extra(key)
        self.make_plot()
        #self.row_count = self.row_count + 1

    def make_plot(self):
        if self.plot:
            self.plot.destroy()
        plot = ZimPlot(self, self.z, title= self.selected_key, cmap= self.combo_cmap.get())
        plot.grid(row=self.row_count, column=0, columnspan=5,)

    def make_extra(self, key):
        data_list = [ np.array(self.model.read_radial_data(file)[key]) for file in self.radial_data_list]
        z = np.row_stack(data_list)
        return np.transpose(z)

    def make_test(self):
        dx, dy = 0.015, 0.05
        y, x = np.mgrid[slice(-4, 4 + dy, dy),
                slice(-4, 4 + dx, dx)]
        z = (1 - x / 3. + x ** 5 + y ** 5) * np.exp(-x ** 2 - y ** 2)
        z = z[:-1, :-1]        
        return z


class Navigator(NavigationToolbar2Tk):
    on_cross = None
    def mouse_move(self, event):
        #self._set_cursor(event)
        if event.button == None: return
        if event.inaxes and event.inaxes.get_navigate():
            try:
                s = event.inaxes.format_coord(event.xdata, event.ydata)
                print(s)
                if self.on_cross:
                    self.on_cross(event.xdata, event.ydata)
                self.set_message(s)
            except (ValueError, OverflowError):
                pass
        else:
            self.set_message(self.mode)
            

class ZimPlot(ttk.Frame):
    def __init__(self, master, z, title, cmap) -> None:
        super().__init__(master)  
        self.fig = plt.figure(figsize=(11, 5), dpi=100)
        axd = self.fig.subplots()
                                    
        axd.set_title(title)
        im = axd.imshow(z, cmap=cmap)  #, extent=[self.z_min, self.z_max, self.y_min, self.y_max])    
        divider = make_axes_locatable(axd)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        plt.colorbar(im, cax=cax)

        self.canvas = FigureCanvasTkAgg(self.fig, self)   
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=1, column=0)
        frame = ttk.Frame(self)
        frame.grid(row=0, column=0, sticky=tk.W)
        toobar = Navigator(self.canvas, frame) 

    def destroy(self):
        print("ZimPlot destroy")
        if self.fig:
            plt.close(self.fig)
        super().destroy()          