import tkinter as tk
import tkinter.ttk as ttk
import numpy as np
import pandas as pd
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

class CheckButtun(tk.Frame):
    def __init__(self, master, title, value, command):
        super().__init__(master)
        self.chkvar = tk.IntVar(name= title, value= value)
        chkbtn = tk.Checkbutton(self, text= title, variable= self.chkvar, command= command)
        chkbtn.pack( pady=5, side=tk.LEFT)

    def get(self):
        return True if self.chkvar.get() == 1 else False
    
class TrajectoryPlotOptionWindows():
    def __init__(self, master, plot_options, on_update_options= None) -> None:
        self.master = master
        self.plot_options = plot_options
        self.on_update_options = on_update_options
  
 

    def show(self):
        win = tk.Toplevel(self.master)
        win.title("Settings")
        win.geometry("220x500")

        self.chk_btn_0 = CheckButtun(win, 'show grid', self.plot_options['show_grid'], self.check_clicked)
        self.chk_btn_0.pack(padx=5, pady=1, fill=tk.X)

        self.chk_btn_1 = CheckButtun(win, 'show marker', self.plot_options['show_marker'], self.check_clicked)
        self.chk_btn_1.pack(padx=5, pady=1, fill=tk.X)

        self.chk_btn_5 = CheckButtun(win, 'show axis labels', self.plot_options['show_axis_labels'], self.check_clicked)
        self.chk_btn_5.pack(padx=5, pady=1, fill=tk.X)

        self.chk_btn_2 = CheckButtun(win, 'show graph', self.plot_options['show_graph'], self.check_clicked)
        self.chk_btn_2.pack(padx=5, pady=1, fill=tk.X)

        self.chk_btn_3 = CheckButtun(win, 'show trajectory', self.plot_options['show_trajectory'], self.check_clicked)
        self.chk_btn_3.pack(padx=5, pady=1, fill=tk.X)

        self.chk_btn_4 = CheckButtun(win, 'show power density', self.plot_options['show_power_density'], self.check_clicked)
        self.chk_btn_4.pack(padx=5, pady=1, fill=tk.X)

        self.chk_btn_6 = CheckButtun(win, 'show power density2', self.plot_options['show_power_density2'], self.check_clicked)
        self.chk_btn_6.pack(padx=5, pady=1, fill=tk.X)        

        frame = tk.Frame(win)
        frame.pack(padx=5, pady=1, fill=tk.X)
        tk.Label(frame, text =f"x axis" ).pack(pady=5, side=tk.LEFT)
        self.combo1 = ttk.Combobox(frame, width= 20 )# command=lambda x=self: self.update(x))  
        self.combo1.bind("<<ComboboxSelected>>", self.combo_selected1)
        self.combo1['values'] =  self.plot_options['term_list']
        self.combo1.current(self.plot_options['term_list'].index(self.plot_options['x_axis']))
        self.combo1.pack(padx=5, pady=5, side=tk.LEFT, fill=tk.X)

        frame = tk.Frame(win)
        frame.pack(padx=5, pady=1, fill=tk.X)
        tk.Label(frame, text =f"y axis" ).pack(pady=5, side=tk.LEFT, fill=tk.X)
        self.combo2 = ttk.Combobox(frame, width= 20 )# command=lambda x=self: self.update(x))  
        self.combo2.bind("<<ComboboxSelected>>", self.combo_selected2)
        self.combo2['values'] =  self.plot_options['term_list']
        self.combo2.current(self.plot_options['term_list'].index(self.plot_options['y_axis']))
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
        self.plot_options['show_grid']          = self.chk_btn_0.get() 
        self.plot_options['show_marker']        = self.chk_btn_1.get() 
        self.plot_options['show_graph']         = self.chk_btn_2.get() 
        self.plot_options['show_trajectory']    = self.chk_btn_3.get()
        self.plot_options['show_power_density'] = self.chk_btn_4.get()
        self.plot_options['show_power_density2'] = self.chk_btn_6.get()        
        self.plot_options['show_axis_labels']   = self.chk_btn_5.get()
                
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

def default_plot_options():
    return { 
        'show_grid' : False,
        'show_marker' : False,
        'show_axis_labels' : False,
        'show_graph' : False,
        'show_trajectory' : True,
        'show_power_density' : False,
        'show_power_density2' : False,
        'term_list' : [],
        'x_axis' : 'theta',
        'y_axis' : 'N_par',
        'cut_index' : 1000,
        'max_index' : 2000
    }
class TrajectoryPlot_v2(ttk.Frame):

    def __init__(self, master, traj_model: TrajectoryModel, plasma_bound) -> None:
        super().__init__(master)  
        self.plasma_bound = plasma_bound
        self.time_stamp = traj_model.time_stamp
        self.traj_model = traj_model
        self.plot_options = default_plot_options()
        self.traj_model.update_theta_interval()
        self.traj_model.update_spectrum_interval()
        self.min_theta = self.traj_model.min_theta
        self.max_theta = self.traj_model.max_theta
        self.min_spectrum_index = self.traj_model.min_spectrum_index
        self.max_spectrum_index = self.traj_model.max_spectrum_index

        self.plot_options['term_list'] =  self.traj_model.get_term_list()
        self.plot_options['max_index'] =  max([len(x['traj']) for x in self.traj_model.traj_series if x['mbad'] == 0] )
        self.plot_options['cut_index'] = self.plot_options['max_index']
        self.show_graph = self.plot_options['show_graph']
        self.show_trajectory = self.plot_options['show_trajectory']
        self.show_power_density = self.plot_options['show_power_density']
        self.show_power_density2 = self.plot_options['show_power_density2']
        self.show_axis_labels = self.plot_options['show_axis_labels']
        # Make a list of colors cycling through the default series.
        self.colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
        self.colormaps = mpl.colormaps['nipy_spectral'] # plasma, tab20, gist_rainbow, rainbow

        self.label1 = tk.Label(master=self, text=f'Theta ({self.traj_model.min_theta}, {self.traj_model.max_theta})')
        self.label1.grid(row=0, column=1, padx=5, sticky=tk.N + tk.S + tk.E + tk.W) 

        if self.traj_model.max_theta>self.traj_model.min_theta:
            slider1 = Slider(self, height = 35, width=330,
                            min_val = self.min_theta, 
                            max_val =  self.max_theta, 
                            init_lis = [self.min_theta, self.max_theta], 
                            show_value = True)
            slider1.grid(row=1, column=1,  sticky=tk.N + tk.S + tk.E + tk.W) 
            slider1.setValueChageCallback(self.update_theta)

        ms = self.traj_model.min_spectrum_index
        gs = self.traj_model.max_spectrum_index
        self.label2 = tk.Label(master=self, text=f'Spectrum ({ms}, {gs})')
        self.label2.grid(row=0, column=2, padx=5, sticky=tk.N + tk.S + tk.E + tk.W) 
        slider2 = Slider(self, height = 35, width=330, min_val = ms, max_val = gs, init_lis = [ms,gs], show_value = True)
        slider2.grid(row=1, column=2, sticky=tk.N + tk.S + tk.E + tk.W) 
        slider2.setValueChageCallback(self.update_spectrum_index)

        self.fig = plt.figure(figsize=(6,6))
        #self.fig.title(time_stamp)
        self.init_axis()
        self.draw_all()
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

    def save_figure(self, file_name):
        self.fig.savefig(file_name)

    def update_spectrum_index(self, vals):
        print(vals)
        self.min_spectrum_index = vals[0]
        self.max_spectrum_index = vals[1]
        #self.label2.config(text = f'Spectrum {self.min_spectrum_index}, {self.max_spectrum_index}')
        self.update()

    def update_theta(self, vals):
        print(vals)
        self.min_theta = vals[0]
        self.max_theta = vals[1]
        #self.label1.config(text = f'Theta ({self.min_theta}, {self.max_theta}')
        self.update()

    def init_axis(self):
        line_1 = []
        if self.show_trajectory:
            line_1.append('trajectory')
        if self.show_power_density:
            line_1.append('power')
        if self.show_power_density2:
            line_1.append('power2')            
        line_2 = []
        if self.show_graph:
            if len(line_1)>1:
                line_2 = ['graph']*len(line_1)
            else:
                line_2 = ['graph']
        mosaic = []
        if len(line_1)>0: mosaic.append(line_1)
        if len(line_2)>0: mosaic.append(line_2)
        # mosaic = [['trajectory', 'power'],
        #               ['graph', 'graph']]
        if len(mosaic)>0:
            self.axd = self.fig.subplot_mosaic(mosaic)
        else:
            self.axd ={}


    def draw_all(self, save_lim= False):
        if self.show_graph:
            self.draw_graphics(self.axd['graph'])

        if self.show_trajectory:
            ax = self.axd['trajectory']
            ax.set_title(self.time_stamp, fontsize=10)
            ax.axis('equal')
            self.draw_trajctory(ax, save_lim)

        if self.show_power_density:
            ax = self.axd['power']
            ax.set_title(self.time_stamp, fontsize=10)
            ax.axis('equal')
            self.draw_power_density(ax)

        if self.show_power_density2:
            ax = self.axd['power2']
            ax.set_title(self.time_stamp, fontsize=10)
            ax.axis('equal')
            self.draw_power_density2(ax)

    def clear_axis(self):
        for key, ax in self.axd.items():
            if ax:
                ax.remove()

    def show_option_windows(self):
        self.option_windows = TrajectoryPlotOptionWindows(self, self.plot_options, self.update_plot_options)
        self.option_windows.show()

    def update_plot_options(self):

        need_update_fig = False
        if self.show_graph != self.plot_options['show_graph']:
            need_update_fig = True
        if self.show_trajectory != self.plot_options['show_trajectory']:
            need_update_fig = True
        if self.show_power_density != self.plot_options['show_power_density']:
            need_update_fig = True
        if self.show_power_density2 != self.plot_options['show_power_density2']:
            need_update_fig = True            
        if self.show_axis_labels != self.plot_options['show_axis_labels']:
            need_update_fig = True            

        self.show_graph = self.plot_options['show_graph']
        self.show_trajectory = self.plot_options['show_trajectory']            
        self.show_power_density = self.plot_options['show_power_density']
        self.show_power_density2 = self.plot_options['show_power_density2']
        self.show_axis_labels = self.plot_options['show_axis_labels']

        if need_update_fig:
            print('nees update fig')
            self.clear_axis()
            self.init_axis()
        
        self.draw_all()
        self.canvas.draw()

    def divider2(self, ray: pd.DataFrame, x_axis, y_axis):
        match x_axis:
            case 'index':
                curve = np.column_stack([ray.index, ray[y_axis]])
                if self.plot_options['show_marker']:
                    if 'driver' in ray.columns:
                        ray2 = ray[ray['driver'] == 2]
                        ray4 = ray[ray['driver'] == 4]
                        driver4_points = np.column_stack([ray4.index, ray4[y_axis]])
                        driver2_points = np.column_stack([ray2.index, ray2[y_axis]])
                    else:
                        driver4_points = np.empty([0, 2], dtype=float)
                        driver2_points = curve
                else:
                    driver4_points = np.empty([0, 2], dtype=float)
                    driver2_points = np.empty([0, 2], dtype=float)
            case _:
                curve = np.column_stack([ray[x_axis], ray[y_axis]])
                if self.plot_options['show_marker']:
                    if 'driver' in ray.columns:
                        ray2 = ray[ray['driver'] == 2]
                        ray4 = ray[ray['driver'] == 4]
                        driver4_points = np.column_stack([ray4[x_axis], ray4[y_axis]])
                        driver2_points = np.column_stack([ray2[x_axis], ray2[y_axis]])
                    else:
                        driver4_points = np.empty([0, 2], dtype=float)
                        driver2_points = curve
                else:
                    driver4_points = np.empty([0, 2], dtype=float)
                    driver2_points = np.empty([0, 2], dtype=float)
        return curve, driver2_points, driver4_points
    
    def draw_graphics(self, axis, save_lim= False):
        '''рисавание графиков значений вдоль луча'''
        bottom, top = axis.get_ylim()
        left, right = axis.get_xlim()  
        axis.clear()
        x_axis = self.plot_options['x_axis']
        y_axis = self.plot_options['y_axis']
        cut_index = self.plot_options['cut_index']
        axis.set_ylabel(y_axis, fontsize=10)
        axis.set_xlabel(x_axis, fontsize=10)
        segs = []
        segs_colors = []
        driver2_list = []
        driver4_list = []

        for series in self.get_good_traj():
            curve, driver2_points, driver4_points= self.divider2(series['traj'].iloc[:cut_index], x_axis, y_axis)
            segs.append(curve)
            driver2_list.append(driver2_points)
            driver4_list.append(driver4_points)                    
            segs_colors.append(self.theta_color(series['theta']))
            segs.append(curve) 
         
        col = collections.LineCollection(segs, colors=segs_colors, alpha=0.5, linewidth=0.5)
        axis.add_collection(col, autolim=True)     

        if self.plot_options['show_marker']:
            for dr2, dr4, clr in zip(driver2_list, driver4_list, segs_colors):
                stars, tri = self.create_markers(dr2, dr4, clr, axis.transData)
                axis.add_collection(stars, autolim=True)            
                axis.add_collection(tri, autolim=True)  

        if save_lim:
            axis.set_ylim(bottom, top)
            axis.set_xlim(left, right)                      
        else: 
            axis.autoscale_view()                           

    def check_theta_lim(self, theta):
        return (self.min_theta <= theta) and (theta <= self.max_theta)
    
    def check_spectrum_lim(self, index):
        return (self.min_spectrum_index <= index) and (index <= self.max_spectrum_index)

    def theta_color(self, theta):
        if self.traj_model.max_theta>self.traj_model.min_theta:
            t = (theta-self.traj_model.min_theta)/(self.traj_model.max_theta-self.traj_model.min_theta)
            return self.colormaps(t)
        else:
            return mpl.colors.to_rgba('#0000F0',0.1)

    
    def divider(self, ray: pd.DataFrame):
        curve = np.column_stack([ray['R'], ray['Z']])
        if self.plot_options['show_marker']:
            if 'driver' in ray.columns:
                ray2 = ray[ray['driver'] == 2]
                ray4 = ray[ray['driver'] == 4]
                driver4_points = np.column_stack([ray4['R'], ray4['Z']])
                driver2_points = np.column_stack([ray2['R'], ray2['Z']])
            else:
                driver4_points = np.empty([0, 2], dtype=float)
                driver2_points = curve
        else:
            driver4_points = np.empty([0, 2], dtype=float)
            driver2_points = np.empty([0, 2], dtype=float)
        return curve, driver2_points, driver4_points

    def get_good_traj(self):
        return ( series for series in self.traj_model.traj_series 
                if self.check_theta_lim(series['theta'])
                if self.check_spectrum_lim(series['index'])   
                if not series['traj'] is None )
    
    def create_markers(self, dr2, dr4, clr, offset_transform):
        stars = collections.RegularPolyCollection(
                                            numsides=5, # a pentagon
                                            sizes=(5,),
                                            facecolors= (clr,),
                                            edgecolors= (clr,),
                                            linewidths= (1,),
                                            offsets= dr2,
                                            offset_transform=offset_transform,
                                            )

        tri = collections.RegularPolyCollection(
                                            numsides=3, # a triangle
                                            sizes=(15,),
                                            facecolors= (clr,),
                                            edgecolors= (clr,),
                                            linewidths= (1,),
                                            offsets= dr4,
                                            offset_transform=offset_transform,
                                            )   
        return stars, tri
    
    def make_color_seg(self, ray: pd.DataFrame):
        points = np.array([ray['R'], ray['Z']]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        #colors = (0.0, 0.0, 1.0, ray['power_density']/30)
        cut_index = self.plot_options['cut_index']
        rgba = list(zip(np.zeros(cut_index), np.zeros(cut_index), np.ones(cut_index), ray['power_density']/25))
        #rgba = list(zip(np.zeros(cut_index), np.zeros(cut_index), np.ones(cut_index), np.ones(cut_index)))
        return segments, rgba

    def make_color_seg_P_tot(self, ray: pd.DataFrame):
        points = np.array([ray['R'], ray['Z']]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        #colors = (0.0, 0.0, 1.0, ray['power_density']/30)
        
        p_tot = np.array(ray['P_tot'])
        cut_index = len(p_tot) #self.plot_options['cut_index']
        one  = np.ones(cut_index)
        zero = np.zeros(cut_index)
        #b = one - np.array(p_tot)
        #a = np.full(cut_index, 0.2)
        b = one
        a = (one - np.array(p_tot))/20

        rgba = list(zip(zero, zero, b, a))
        #rgba = list(zip(np.zeros(cut_index), np.zeros(cut_index), np.ones(cut_index), np.ones(cut_index)))
        return segments, rgba

    def draw_poloidal_view(self, axis, save_lim= False):
        if self.show_power_density: 
            self.draw_power_density(axis)
        else:
            self.draw_trajctory(axis, save_lim)

    def draw_power_density(self, axis):
        axis.clear()
        axis.plot(self.plasma_bound['R'], self.plasma_bound['Z'])
        cut_index = self.plot_options['cut_index']

        for series in self.get_good_traj():
            segments, colors = self.make_color_seg(series['traj'].iloc[:cut_index])
            col = collections.LineCollection(segments, colors= colors, linewidth=0.5)
            axis.add_collection(col, autolim=True)

        if self.plot_options['show_grid']:
                axis.grid(visible= True)

        if self.plot_options['show_axis_labels']:
            axis.set_xlabel('R [m]')
            axis.set_ylabel('Z [m]')

        axis.autoscale_view()

    def draw_power_density2(self, axis):
        axis.clear()
        axis.plot(self.plasma_bound['R'], self.plasma_bound['Z'])
        cut_index = self.plot_options['cut_index']

        for series in self.get_good_traj():
            segments, colors = self.make_color_seg_P_tot(series['traj'].iloc[:cut_index])
            col = collections.LineCollection(segments, colors= colors, linewidth=0.5)
            axis.add_collection(col, autolim=True)

        if self.plot_options['show_grid']:
                axis.grid(visible= True)

        if self.plot_options['show_axis_labels']:
            axis.set_xlabel('R [m]')
            axis.set_ylabel('Z [m]')

        axis.autoscale_view()


    def draw_trajctory(self, axis, save_lim= False):
        
        bottom, top = axis.get_ylim()
        left, right = axis.get_xlim()        

        axis.clear()
        axis.plot(self.plasma_bound['R'], self.plasma_bound['Z'])

        cut_index = self.plot_options['cut_index']

        segs = []
        segs_colors = []
        driver2_list = []
        driver4_list = []
        for series in self.get_good_traj():
            curve, driver2_points, driver4_points= self.divider(series['traj'].iloc[:cut_index])
            segs.append(curve)
            driver2_list.append(driver2_points)
            driver4_list.append(driver4_points)
            segs_colors.append(self.theta_color(series['theta']))

        col = collections.LineCollection(segs, colors=segs_colors, alpha=0.5, linewidth=0.5)
        axis.add_collection(col, autolim=True)
        
        if self.plot_options['show_marker']:
            for dr2, dr4, clr in zip(driver2_list, driver4_list, segs_colors):
                stars, tri = self.create_markers(dr2, dr4, clr, axis.transData)
                axis.add_collection(stars, autolim=True)            
                axis.add_collection(tri, autolim=True)  

        if self.plot_options['show_grid']:
                axis.grid(visible= True)

        if self.plot_options['show_axis_labels']:
            axis.set_xlabel('R [m]')
            axis.set_ylabel('Z [m]')

        if save_lim:
            axis.set_ylim(bottom, top)
            axis.set_xlim(left, right)                      
        else:
            axis.autoscale_view()

    def update(self):
        self.time_stamp = self.traj_model.time_stamp
        self.draw_all(save_lim= True)
        self.canvas.draw()


    def destroy(self):
        if self.fig:
            plt.close(self.fig)
        super().destroy()   