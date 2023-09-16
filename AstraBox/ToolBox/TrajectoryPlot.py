import tkinter as tk
import tkinter.ttk as ttk
import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib import collections, transforms

from matplotlib.backends.backend_tkagg import ( FigureCanvasTkAgg, NavigationToolbar2Tk)
from AstraBox.ToolBox.VerticalNavigationToolbar import VerticalNavigationToolbar2Tk
import AstraBox.ToolBox.ImageButton as ImageButton

class TrajectoryPlotOptionWindows():
    def __init__(self, master, plot_options, on_update_options= None) -> None:
        self.master = master
        self.plot_options = plot_options
        self.on_update_options = on_update_options
  
 

    def show(self):
        win = tk.Toplevel(self.master)
        win.title("Settings")
        win.geometry("220x400")

        var = tk.IntVar(name= 'show ax2', value= self.plot_options['axis2'])
        chkbtn = tk.Checkbutton(win, text='show ax2', variable=var, command= self.check_clicked )
        chkbtn.pack(padx=5, pady=5, fill=tk.X)

        fr1 = tk.Frame(win)
        fr1.pack(padx=5, pady=1, fill=tk.X)
        tk.Label(fr1, text =f"x axis" ).pack(padx=5, pady=5, side=tk.LEFT)
        self.combo1 = ttk.Combobox(fr1, width= 20 )# command=lambda x=self: self.update(x))  
        self.combo1.bind("<<ComboboxSelected>>", self.combo_selected1)
        self.combo1['values'] =  self.plot_options['term_list']
        self.combo1.current(self.plot_options['term_list'].index('theta'))
        self.combo1.pack(padx=5, pady=5, side=tk.LEFT, fill=tk.X)

        fr2 = tk.Frame(win)
        fr2.pack(padx=5, pady=1, fill=tk.X)
        tk.Label(fr2, text =f"y axis" ).pack(padx=5, pady=5, side=tk.LEFT, fill=tk.X)
        self.combo2 = ttk.Combobox(fr2, width= 20 )# command=lambda x=self: self.update(x))  
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

    def check_clicked(self):
        pass

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

class TrajectoryPlot(ttk.Frame):
    plot_options = { 
        'axis2' : 0 ,
        'term_list' : ['ab','cd'],
        'x_axis' : 'theta',
        'y_axis' : 'N_par',
        'cut_index' : 10,
        'max_index' : 200
    }
    def __init__(self, master, rays, time_stamp, plasma_bound) -> None:
        super().__init__(master)  
        self.plasma_bound = plasma_bound
        self.rays = rays
        self.plot_options['term_list'] = ['ray_index', 'index'] + list(rays[0].keys())
        self.plot_options['max_index'] =  max([len(ray['theta']) for ray in self.rays])
                    
        self.option_windows = TrajectoryPlotOptionWindows(self, self.plot_options, self.update_plot_options)
        self.fig = plt.figure(figsize=(6,6))
        #self.fig.title(time_stamp)
        self.ax1, self.ax2 = self.fig.subplots(2, 1)
        self.ax1.set_title(time_stamp, fontsize=12)
        self.ax1.axis('equal')
        self.ax1.plot(self.plasma_bound['R'], self.plasma_bound['Z'])
        for ray in rays:
            self.ax1.plot(ray['R'], ray['Z'], alpha=0.5, linewidth=0.5)

        self.ax2.set_title('N_par', fontsize=12)
        self.ax2.set_xlabel('theta', fontsize=12)
        for ray in rays:
            self.ax2.plot(ray['theta'], ray['N_par'], alpha=0.5, linewidth=0.5)

        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=1)
        #toobar = NavigationToolbar2Tk(self.canvas, self, pack_toolbar=False)
        #toobar.grid(row=0, column=0, sticky=tk.W)
        tb = VerticalNavigationToolbar2Tk(self.canvas, self)
        tb.update()
        tb.grid(row=0, column=0, sticky=tk.N)    
        btn = ImageButton.create(self, '4231901.png', self.show_option_windows)
        btn.grid(row=1, column=0, sticky=tk.N) 
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

    def show_option_windows(self):
        self.option_windows.show()

    def update_plot_options(self):
        self.update_rays()
        self.update_axis2()
        self.canvas.draw()


    def update_axis2(self):
        self.ax2.clear()
        x_axis = self.plot_options['x_axis']
        y_axis = self.plot_options['y_axis']
        cut_index = self.plot_options['cut_index']
        self.ax2.set_ylabel(y_axis, fontsize=12)
        self.ax2.set_xlabel(x_axis, fontsize=12)
        match x_axis:
            case 'ray_index':
                rl = len(self.rays)
                for id, ray in enumerate(self.rays):
                    ci = len(ray[y_axis][0:cut_index])
                    ri = np.full((ci), id)
                    #print(ri)
                    #print(ray[y_axis][0:cut_index])
                    if cut_index>3:
                        self.ax2.plot(ri, ray[y_axis][0:cut_index], alpha=0.5, linewidth=1.5)         
                    else:
                        self.ax2.plot(ri, ray[y_axis][0:cut_index], marker='o', markersize= 1, alpha=0.5, linewidth=1.5)         
            case 'index':
                for ray in self.rays:
                    if cut_index>3:
                        self.ax2.plot(ray[y_axis][0:cut_index], alpha=0.5, linewidth=0.5)         
                    else:
                        self.ax2.plot(ray[y_axis][0:cut_index], marker='o', markersize= 1, alpha=0.5, linewidth=0.5)         
            case _:
                for ray in self.rays:
                    if cut_index>3:
                        self.ax2.plot(ray[x_axis][0:cut_index], ray[y_axis][0:cut_index], alpha=0.5, linewidth=0.5)
                    else:
                        self.ax2.plot(ray[x_axis][0:cut_index], ray[y_axis][0:cut_index], marker='o', markersize= 1, alpha=0.5, linewidth=0.5)         
        self.canvas.draw()

    def update_rays(self):
        bottom, top = self.ax1.get_ylim()
        left, right = self.ax1.get_xlim()        

        # Make a list of colors cycling through the default series.
        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
        self.ax1.clear()
        self.ax1.plot(self.plasma_bound['R'], self.plasma_bound['Z'])
        cut_index = self.plot_options['cut_index']
        segs = []
        for ray in self.rays:
            curve = np.column_stack([ray['R'][0:cut_index], ray['Z'][0:cut_index]])
            segs.append(curve)
        col = collections.LineCollection(segs, colors=colors, alpha=0.5, linewidth=0.5)
        self.ax1.add_collection(col, autolim=True)
        
        #if cut_index>3:
        #    for ray in self.rays:
        #        self.ax1.plot(ray['R'][0:cut_index], ray['Z'][0:cut_index], alpha=0.5, linewidth=0.5)        
        #else:
        #    for ray in self.rays:
        #        self.ax1.plot(ray['R'][0:cut_index], ray['Z'][0:cut_index], marker='o', markersize= 1,  alpha=0.5, linewidth=0.5)     
        self.ax1.set_ylim(bottom, top)
        self.ax1.set_xlim(left, right)                      

    def update(self, rays, time_stamp):
        self.rays = rays
        self.update_rays()
        self.ax1.set_title(time_stamp, fontsize=12)
    
        self.update_axis2()



    def destroy(self):
        if self.fig:
            plt.close(self.fig)
        super().destroy()   