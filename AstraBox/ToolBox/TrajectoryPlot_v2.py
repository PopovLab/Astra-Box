import tkinter as tk
import tkinter.ttk as ttk
import numpy as np
import matplotlib as mpl
from matplotlib.colors import LinearSegmentedColormap, ListedColormap
from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib import collections, transforms

from matplotlib.backends.backend_tkagg import ( FigureCanvasTkAgg, NavigationToolbar2Tk)
from AstraBox.ToolBox.VerticalNavigationToolbar import VerticalNavigationToolbar2Tk
import AstraBox.ToolBox.ImageButton as ImageButton
from AstraBox.Models.TrajectoryModel import TrajectoryModel

from AstraBox.Views.tkSliderWidget import Slider

class TrajectoryPlotOptionWindows():
    def __init__(self, master, plot_options, on_update_options= None) -> None:
        self.master = master
        self.plot_options = plot_options
        self.on_update_options = on_update_options
  
 

    def show(self):
        win = tk.Toplevel(self.master)
        win.title("Settings")
        win.geometry("220x400")

        frame = tk.Frame(win)
        frame.pack(padx=5, pady=1, fill=tk.X)
        self.chkvar1 = tk.IntVar(name= 'show marker', value= self.plot_options['show_marker'])
        chkbtn = tk.Checkbutton(frame, text='show marker', variable= self.chkvar1, command= self.check_clicked )
        chkbtn.pack( pady=5, side=tk.LEFT)

        frame = tk.Frame(win)
        frame.pack(padx=5, pady=1, fill=tk.X)
        self.chkvar2 = tk.IntVar(name= 'show graph', value= self.plot_options['show_graph'])
        chkbtn = tk.Checkbutton(frame, text='show graph', variable= self.chkvar2, command= self.check_clicked )
        chkbtn.pack( pady=5, side=tk.LEFT)

        frame = tk.Frame(win)
        frame.pack(padx=5, pady=1, fill=tk.X)
        tk.Label(frame, text =f"x axis" ).pack(pady=5, side=tk.LEFT)
        self.combo1 = ttk.Combobox(frame, width= 20 )# command=lambda x=self: self.update(x))  
        self.combo1.bind("<<ComboboxSelected>>", self.combo_selected1)
        self.combo1['values'] =  self.plot_options['term_list']
        self.combo1.current(self.plot_options['term_list'].index('theta'))
        self.combo1.pack(padx=5, pady=5, side=tk.LEFT, fill=tk.X)

        frame = tk.Frame(win)
        frame.pack(padx=5, pady=1, fill=tk.X)
        tk.Label(frame, text =f"y axis" ).pack(pady=5, side=tk.LEFT, fill=tk.X)
        self.combo2 = ttk.Combobox(frame, width= 20 )# command=lambda x=self: self.update(x))  
        self.combo2.bind("<<ComboboxSelected>>", self.combo_selected2)
        self.combo2['values'] =  self.plot_options['term_list']
        self.combo2.current(self.plot_options['term_list'].index('N_par'))
        self.combo2.pack(padx=5, pady=5, side=tk.LEFT, fill=tk.X)

        self.cut_index_var = tk.IntVar(value= self.plot_options['cut_index'])
        self.cut_index_var.trace_add('write', self.update_index)
        self.hs = tk.Scale(win, 
                       variable = self.cut_index_var, 
                       label='Cut index',
                       orient=tk.HORIZONTAL,
                       length=200, 
                       tickinterval = 100,
                       from_= 1, 
                       to= self.plot_options['max_index'] )
        self.hs.pack(padx=5, pady=5, fill=tk.X)
        win.grab_set()
        win.focus_set()
        win.wait_window()

    def check_clicked(self):
        self.plot_options['show_marker'] = True if self.chkvar1.get() == 1 else False
        self.plot_options['show_graph'] = True if self.chkvar2.get() == 1 else False
        if self.on_update_options:
            self.on_update_options()

    def combo_selected1(self, *args):
        print(self.combo1.get())
        self.plot_options['x_axis'] = self.combo1.get()
        if self.on_update_options:
            self.on_update_options()

    def combo_selected2(self, *args):
        print(self.combo1.get())
        self.plot_options['y_axis'] = self.combo2.get()
        if self.on_update_options:
            self.on_update_options()

    def update_index(self, *args):
        self.plot_options['cut_index'] = self.cut_index_var.get()
        print(self.cut_index_var.get())
        if self.on_update_options:
            self.on_update_options()

class TrajectoryPlot_v2(ttk.Frame):
    plot_options = { 
        'show_marker' : False,
        'show_graph' : False,
        'term_list' : [],
        'x_axis' : 'theta',
        'y_axis' : 'N_par',
        'cut_index' : 1000,
        'max_index' : 2000
    }
    def __init__(self, master, traj_model: TrajectoryModel, plasma_bound) -> None:
        super().__init__(master)  
        self.plasma_bound = plasma_bound
        self.time_stamp = traj_model.time_stamp
        self.traj_model = traj_model

        self.traj_model.update_theta_interval()
        self.traj_model.update_spectrum_interval()
        self.min_theta = self.traj_model.min_theta
        self.max_theta = self.traj_model.max_theta
        self.min_spectrum_index = self.traj_model.min_spectrum_index
        self.max_spectrum_index = self.traj_model.max_spectrum_index

        #self.plot_options['term_list'] = ['ray_index', 'index'] + list(rays[0].keys())
        #self.plot_options['max_index'] =  max([len(ray['theta']) for ray in self.rays])
        self.plot_options['cut_index'] = self.plot_options['max_index']
        self.show_graph = self.plot_options['show_graph']
        # Make a list of colors cycling through the default series.
        self.colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
        self.colormaps = mpl.colormaps['nipy_spectral'] # plasma, tab20, gist_rainbow, rainbow

        self.label1 = tk.Label(master=self, text=f'Theta ({self.traj_model.min_theta}, {self.traj_model.max_theta}')
        self.label1.grid(row=0, column=1, padx=5, sticky=tk.N + tk.S + tk.E + tk.W) 

        slider1 = Slider(self, height = 35, width=350,
                         min_val = self.min_theta, 
                         max_val =  self.max_theta, 
                         init_lis = [self.min_theta, self.max_theta], 
                         show_value = True)
        slider1.grid(row=1, column=1,  sticky=tk.N + tk.S + tk.E + tk.W) 
        slider1.setValueChageCallback(self.update_theta)

        ms = self.traj_model.min_spectrum_index
        gs = self.traj_model.max_spectrum_index
        self.label2 = tk.Label(master=self, text='Spectrum {ms}, {gs}')
        self.label2.grid(row=0, column=2, padx=5, sticky=tk.N + tk.S + tk.E + tk.W) 
        slider2 = Slider(self, height = 35, min_val = ms, max_val = gs, init_lis = [ms,gs], show_value = True)
        slider2.grid(row=1, column=2, sticky=tk.N + tk.S + tk.E + tk.W) 
        slider2.setValueChageCallback(self.update_spectrum_index)


        self.ax1 = None
        self.ax2 = None
        self.fig = plt.figure(figsize=(6,6))
        #self.fig.title(time_stamp)
        self.init_axis()

        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=2, column=1,columnspan=2, rowspan= 3, sticky=tk.N + tk.S + tk.E + tk.W)
        #toobar = NavigationToolbar2Tk(self.canvas, self, pack_toolbar=False)
        #toobar.grid(row=0, column=0, sticky=tk.W)
        tb = VerticalNavigationToolbar2Tk(self.canvas, self)
        tb.update()
        tb.grid(row=2, column=0, sticky=tk.N)    
        lbl = tk.Label(master=self, text='v2')
        lbl.grid(row=3, column=0, sticky=tk.N) 
        btn = ImageButton.create(self, 'gear.png', self.show_option_windows)
        btn.grid(row=4, column=0, sticky=tk.N) 
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(2, weight=1)


    def update_spectrum_index(self, vals):
        print(vals)
        self.min_spectrum_index = vals[0]
        self.max_spectrum_index = vals[1]
        self.label2.config(text = f'Spectrum {self.min_spectrum_index}, {self.max_spectrum_index}')
        self.update()

    def update_theta(self, vals):
        print(vals)
        self.min_theta = vals[0]
        self.max_theta = vals[1]
        self.label1.config(text = f'Theta ({self.min_theta}, {self.max_theta}')
        self.update()

    def init_axis(self):
        if self.show_graph:
            self.ax1, self.ax2 = self.fig.subplots(2, 1)
            self.ax1.set_title(self.time_stamp, fontsize=10)
            self.ax1.axis('equal')
            self.update_graph()
        else:
            self.ax1 = self.fig.subplots(1, 1)
            self.ax1.set_title(self.time_stamp, fontsize=10)
            self.ax1.axis('equal')
        self.update_traj()


    def clear_axis(self):
        if self.ax1:
            self.ax1.remove()
            self.ax1 = None
        if self.ax2:
            self.ax2.remove()
            self.ax2 = None

    def show_option_windows(self):
        self.option_windows = TrajectoryPlotOptionWindows(self, self.plot_options, self.update_plot_options)
        self.option_windows.show()

    def update_plot_options(self):
        if self.show_graph != self.plot_options['show_graph']:
            self.clear_axis()
            self.show_graph = self.plot_options['show_graph']
            self.init_axis()
        self.update_rays(save_lim= True)
        if self.show_graph:
            self.update_graph()
        self.canvas.draw()


    def update_graph(self):
        self.ax2.clear()
        x_axis = self.plot_options['x_axis']
        y_axis = self.plot_options['y_axis']
        cut_index = self.plot_options['cut_index']
        self.ax2.set_ylabel(y_axis, fontsize=10)
        self.ax2.set_xlabel(x_axis, fontsize=10)
        segs = []
        match x_axis:
            case 'ray_index':
                rl = len(self.rays)
                for id, ray in enumerate(self.rays):
                    ci = len(ray[y_axis][0:cut_index])
                    ri = np.full((ci), id)
                    curve = np.column_stack([ri, ray[y_axis][0:cut_index]])
                    segs.append(curve)         
            case 'index':
                for ray in self.rays:
                    curve = np.column_stack([ray[y_axis].index[0:cut_index], ray[y_axis][0:cut_index]])
                    segs.append(curve)  
            case _:
                for ray in self.rays:
                    curve = np.column_stack([ray[x_axis][0:cut_index], ray[y_axis][0:cut_index]])
                    segs.append(curve) 
         
        col = collections.LineCollection(segs, colors=self.colors, alpha=0.5, linewidth=0.5)
        self.ax2.add_collection(col, autolim=True)     

        if cut_index<5 or self.plot_options['show_marker']:
            cl = len(self.colors)
            for id, sg in enumerate(segs):
                clr = self.colors[id % cl]
                stars = collections.RegularPolyCollection(
                                                    numsides=5, # a pentagon
                                                    sizes=(5,),
                                                    facecolors= (clr,),
                                                    edgecolors= (clr,),
                                                    linewidths= (1,),
                                                    offsets= sg,
                                                    offset_transform=self.ax2.transData,
                                                    )
                self.ax2.add_collection(stars, autolim=True)  
                self.ax2.autoscale_view()   
        self.ax2.autoscale_view()                           

    def check_theta_lim(self, theta):
        return (self.min_theta < theta) and (theta < self.max_theta)
    
    def check_spectrum_lim(self, index):
        return (self.min_spectrum_index < index) and (index < self.max_spectrum_index)

    def theta_color(self, theta):
        t = (theta-self.traj_model.min_theta)/(self.traj_model.max_theta-self.traj_model.min_theta)
        return self.colormaps(t)
        #lc = len(self.colors)
        #return self.colors[int(t*lc)]
    
    def update_traj(self, save_lim= False):
        bottom, top = self.ax1.get_ylim()
        left, right = self.ax1.get_xlim()        

        self.ax1.clear()
        self.ax1.plot(self.plasma_bound['R'], self.plasma_bound['Z'])
        cut_index = self.plot_options['cut_index']
        segs = []
        segs_colors = []
        for series in self.traj_model.traj_series:
            if self.check_theta_lim(series['theta']):
                if self.check_spectrum_lim(series['index']):
                    if not series['traj'] is None:
                        ray = series['traj']
                        #print(len(ray['R']))
                        curve = np.column_stack([ray['R'][0:cut_index], ray['Z'][0:cut_index]])
                        segs.append(curve)
                        segs_colors.append(self.theta_color(series['theta']))
        col = collections.LineCollection(segs, colors=segs_colors, alpha=0.5, linewidth=0.5)
        self.ax1.add_collection(col, autolim=True)
        
        if cut_index<5 or self.plot_options['show_marker']:
            cl = len(self.colors)
            for id, sg in enumerate(segs):
                clr = self.colors[id % cl]
                stars = collections.RegularPolyCollection(
                                                    numsides=5, # a pentagon
                                                    sizes=(5,),
                                                    facecolors= (clr,),
                                                    edgecolors= (clr,),
                                                    linewidths= (1,),
                                                    offsets= sg,
                                                    offset_transform=self.ax1.transData,
                                                    )
                self.ax1.add_collection(stars, autolim=True)  
        if save_lim:
            self.ax1.set_ylim(bottom, top)
            self.ax1.set_xlim(left, right)                      
        else:
            self.ax1.autoscale_view()

    def update(self):
        #self.rays = rays
        self.update_traj(save_lim= True)
        self.ax1.set_title(self.traj_model.time_stamp, fontsize=12)
        if self.show_graph:
            self.update_graph()
        self.canvas.draw()


    def destroy(self):
        if self.fig:
            plt.close(self.fig)
        super().destroy()   