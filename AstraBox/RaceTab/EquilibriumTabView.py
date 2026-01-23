import time
import tkinter as tk
import tkinter.ttk as ttk
from typing import Any
import tkinter.messagebox as messagebox
import matplotlib
import pandas as pd
from matplotlib import cm, collections
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import  FigureCanvasTkAgg, NavigationToolbar2Tk
from AstraBox.Models.TimestampFilesManager import TimestampFilesManager
from AstraBox.Models.TrajectoryModel import TrajectoryModel
from AstraBox.ToolBox.VerticalNavigationToolbar import VerticalNavigationToolbar2Tk

from AstraBox.RaceTab.TabViewBasic import TabViewBasic
from AstraBox.Models.RaceModel import RaceModel
from AstraBox.ToolBox.MaxwellPlot import MaxwellPlot
import numpy as np
from numpy.polynomial import polynomial as P

def polynom(coef):
    return P.Polynomial(coef)

class MagneticConfiguration():
    def __init__(self, equilibrium) -> None:
        self.equilibrium = equilibrium
        self.delta = polynom(self.equilibrium['PROFILE_APPROX']['cdl']) # delta - shift as a function of "minor radius"
        self.ell   = polynom(self.equilibrium['PROFILE_APPROX']['cly']) # ellipticity as a function of "minor radius"
        self.gamma = polynom(self.equilibrium['PROFILE_APPROX']['cgm']) # gamma - triangularity as a function of "minor radius":
        self.amy   = polynom(self.equilibrium['PROFILE_APPROX']['cmy']) # Polinomial approximation of the amy(r) 
                                                     #  amy=(btor/q)*rho*(drho/dr) is a function of "minor radius" r=rh(i).


    def magntic_surface(self, xr, theta):
        rm = self.equilibrium['GEOMETRY']['rm']
        r0 = self.equilibrium['GEOMETRY']['r0']
        z0 = self.equilibrium['GEOMETRY']['z0']
        b_tor = self.equilibrium['FIELDS']['b_tor0']
        #xdl=fdf(xr,cdl,ncoef,xdlp) 
        xdl = self.delta(xr)
        #xly=fdf(xr,cly,ncoef,xlyp)
        xly = self.ell(xr)
        #xgm=fdf(xr,cgm,ncoef,xgmp)
        xgm = self.gamma(xr)

        cotet = np.cos(theta)
        sitet = np.sin(theta)
        xx = -xdl + xr*cotet - xgm*sitet**2
        zz = xr*xly*sitet
        R = (r0 + rm*xx)/100
        Z = (z0 + rm*zz)/100
        return R, Z

class PoloidalPlot(ttk.Frame):

    def __init__(self, master, plasma_bound) -> None:
        super().__init__(master)  
        
        self.plasma_bound = plasma_bound
        self.fig = plt.figure(figsize=(6,6))
        self.axis = self.fig.subplots(1, 1)

        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.get_tk_widget().grid(row=2, column=1,columnspan=2, rowspan= 3, sticky=tk.N + tk.S + tk.E + tk.W)
        #self.update_equilibrium(equilibrium)
        #toobar = NavigationToolbar2Tk(self.canvas, self, pack_toolbar=False)
        #toobar.grid(row=0, column=0, sticky=tk.W)
        tb = VerticalNavigationToolbar2Tk(self.canvas, self)
        tb.update()
        tb.grid(row=2, column=0, sticky=tk.N)    
        lbl = tk.Label(master=self, text='v3')
        lbl.grid(row=3, column=0, sticky=tk.N) 
        #btn = ImageButton.create(self, 'gear.png', self.show_option_windows)
        #btn.grid(row=4, column=0, sticky=tk.N) 
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(2, weight=1)

    def update_equilibrium(self, equilibrium):
        self.axis.clear()
        self.mag_cong = MagneticConfiguration(equilibrium)
        self.init_axis( f"Poloidal view. time={equilibrium['time_stamp']}",
                equilibrium['GEOMETRY']['r0']/100,
                equilibrium['GEOMETRY']['z0']/100)
        self.draw_all()
        self.canvas.draw()

    def init_axis(self, title, x0, y0):
        # Настройки графика
        ax = self.axis
        ax.set_title(title, fontsize=14)
        ax.set_xlabel('R (cm)', fontsize=12)
        ax.set_ylabel('Z (cm)', fontsize=12)
        ax.grid(True, alpha=0.2)
        ax.axhline(y=y0, color='k', alpha=0.3)
        ax.axvline(x=x0, color='k', alpha=0.3)
        ax.set_aspect('equal')
             
    def draw_all(self, save_lim= False):
        self.axis.plot(self.plasma_bound['R'], self.plasma_bound['Z'])        
        theta = np.linspace(0, 2*np.pi, 100)
        for i in range(1,10):
            R, Z = self.mag_cong.magntic_surface(i/10.0, theta)
            self.axis.plot(R, Z, linewidth=1, alpha=0.8)

class PoloidalView(tk.Frame):
    def __init__(self, master, race_model: RaceModel, ) ->None:
        super().__init__(master)  
        self.race_model = race_model
        self.equilibrium_manager = self.race_model.equilibrium_files_manager

        plasma_bound = self.race_model.read_plasma_bound()

        self.plot = PoloidalPlot(self, plasma_bound)
        self.plot.grid(row=0, rowspan= 2, column=0, sticky=tk.N + tk.S + tk.E + tk.W, pady=4, padx=8)
        btn = ttk.Button(self, text= "show pos trajectory", style = 'Toolbutton', command=self.show_pos_traj)
        btn.grid(row=0, column=1, pady=4, padx=8)
        btn = ttk.Button(self, text= "show neg trajectory", style = 'Toolbutton', command=self.show_neg_traj)
        btn.grid(row=1, column=1, pady=4, padx=8)
        start_time, finish_time  =  self.equilibrium_manager.get_timestamp_range()
        self.update_time(start_time)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)    

    def update_time(self, time_stamp: float):
        equilibrium = self.equilibrium_manager.read_nml_file(time_stamp)
        equilibrium['time_stamp'] = time_stamp
        a= equilibrium['PROFILE_APPROX']
        print(a['CDL'][0], a['CLY'][0], a['CGM'][0])
        self.plot.update_equilibrium(equilibrium)
    
    def show_pos_traj(self):    
        print('show_traj')    
        folder_name= 'TRAJ_POS'
        self.traj_model = TrajectoryModel(self.race_model, folder_name)
        print(self.traj_model.num_traj)
        if self.traj_model.num_traj>0: 
            self.traj_model.select_series(0)
            self.traj_model.update_theta_interval()            
            self.draw_trajctory(self.plot.axis)
            self.plot.canvas.draw()

    def show_neg_traj(self):    
        print('show_traj')      
        folder_name= 'TRAJ_NEG'     
        start = time.perf_counter()
        self.traj_model = TrajectoryModel(self.race_model, folder_name)
        print(f'1. create traj_model: {(time.perf_counter() - start):.6f} сек')
        print(self.traj_model.num_traj)
        if self.traj_model.num_traj>0: 
            self.traj_model.select_series(0)
            print(f'2. select_series  {(time.perf_counter() - start):.6f} сек')
            self.traj_model.update_theta_interval()
            print(f'3. update_theta_interval {(time.perf_counter() - start):.6f} сек')
            self.draw_trajctory(self.plot.axis)
            print(f'4. draw_trajctory {(time.perf_counter() - start):.6f} сек')
            self.plot.canvas.draw()

    def get_good_traj(self):
        return ( series for series in self.traj_model.traj_series 
                if not series['traj'] is None )

    def divider(self, ray: pd.DataFrame):
        curve = np.column_stack([ray['R'], ray['Z']])
        return curve
            
    def theta_color(self, theta):
        if self.traj_model.max_theta>self.traj_model.min_theta:
            t = (theta-self.traj_model.min_theta)/(self.traj_model.max_theta-self.traj_model.min_theta)
            return self.colormaps(t)
        else:
            return matplotlib.colors.to_rgba('#0000F0',0.1)
            
    def draw_trajctory(self, axis, save_lim= False):
        self.colormaps = matplotlib.colormaps['nipy_spectral'] # plasma, tab20, gist_rainbow, rainbow
        #bottom, top = axis.get_ylim()
        #left, right = axis.get_xlim()        

        #axis.clear()
        #axis.plot(self.plasma_bound['R'], self.plasma_bound['Z'])

        cut_index = -1 #self.plot_options['cut_index']
        segs = []
        segs_colors = []
        for series in self.get_good_traj():
            curve = self.divider(series['traj'])
            segs.append(curve)
            segs_colors.append(self.theta_color(series['theta']))

        col = collections.LineCollection(segs, colors=segs_colors, alpha=0.5, linewidth=0.5)
        axis.add_collection(col, autolim=True)
        

 

class EquilibriumTabView(TabViewBasic):
    def __init__(self, master, model: RaceModel) -> None:
        super().__init__(master, model)  


    def init_ui(self): 
        equilibrium_manager = self.race_model.equilibrium_files_manager
        if equilibrium_manager.count_files() == 0:
            label = tk.Label(master=self, text='Нет данных')
            label.grid(row=0, column=1, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)     
            return

        start_time, finish_time  =  equilibrium_manager.get_timestamp_range()
        self.n = equilibrium_manager.count_files()
        equilibrium = equilibrium_manager.read_nml_file(start_time)
        print(equilibrium['GEOMETRY'])
        equilibrium['time_stamp'] = start_time
        self.time_var = tk.DoubleVar(master= self, value= start_time)
        self.time_var.trace_add('write', self.update_time_var)
        step = (finish_time-start_time)/self.n
        self.time_slider = tk.Scale(master=  self, 
                                variable = self.time_var,
                                orient = tk.HORIZONTAL,
                                label='Time scale',
                                tickinterval= (finish_time-start_time)/7,
                                from_= start_time,
                                to= finish_time, 
                                resolution= step, 
                                length = 250 )
        self.time_slider.grid(row=1, column=0, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W)       
        
        self.poloidal_view = PoloidalView(self, self.race_model)
        self.poloidal_view.grid(row=2, column=0, sticky=tk.N + tk.S + tk.E + tk.W, pady=4, padx=8)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)            

    def update_time_var(self, var, indx, mode):
        self.poloidal_view.update_time(self.time_var.get())

