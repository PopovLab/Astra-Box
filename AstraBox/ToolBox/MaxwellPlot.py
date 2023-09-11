import tkinter as tk
import tkinter.ttk as ttk
import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import ( FigureCanvasTkAgg, NavigationToolbar2Tk)
from AstraBox.ToolBox.VerticalNavigationToolbar import VerticalNavigationToolbar2Tk

speed_of_light = 3.0e+10
def renorm_maxwell(maxwell, norm_vt_flag = False, energy_scale = False, diff = False):
    X = maxwell['X']
    Y = maxwell['Y']
    vmax = abs(X[0])
    #print(f'min: {X.min()} max: {X.max()} vmax: {vmax}')
    #print(type(X))
    if norm_vt_flag:
        X = 2*X / vmax
    if energy_scale:
        X = X * np.abs(X)
    #Y = Y * vmax /1000 #Эмпирический коэффициент
    #print(np.sum(Y))
    if diff:
        n2 = int(len(X)/2)
        #print(f' {X[n2-3]}  {X[n2-2]}  {X[n2-1]}  {X[n2]}  {X[n2+1]}  {X[n2+2]} ')
        diff_Y = np.abs(np.array([Y[n2-i]-Y[n2+i] for i in range(n2-1)]))
        X = X[n2:n2+n2-1]
        return {'X': X, 'Y': diff_Y}
    n4 = int(len(X)/4)
    n3 = int(3*n4)+2
    return {'X': X[n4:n3], 'Y': Y[n4:n3]}

    #thermal_vel = vmax/speed_of_light/2
    #n = len(X)
    #nl = n//2 - n//8
    #nr = n//2 + n//8
    #YL = Y[nl]
    #YR = Y[nr]
    #XL = X[nl]
    #XR = X[nr]    
    #return {'X': X, 'Y': Y, 'TX': [XL, XR], 'TY': [YL, YR]}

def renorm_series(series, norm_vt_flag = False, energy_scale = False,  diff = False):
    new_series = []
    for item in series:
        new_series.append(renorm_maxwell(item, norm_vt_flag, energy_scale, diff))
    return new_series

class MaxwellPlot(ttk.Frame):
    def __init__(self, master, m_series, title, time_stamp, уscale_log = True) -> None:
        super().__init__(master)  
        self.my_series = m_series
        self.уscale_log = уscale_log
        self.norm_vt_flag = False
        self.energy_scale = False
        self.diff = False
        self.title = title
        self.series = renorm_series(m_series)

        tb = self.make_toolbar()
        tb.grid(row=0, column=0, columnspan=2, sticky=tk.N + tk.S + tk.E + tk.W) 

        self.fig = plt.figure(figsize=(8, 5))
        self.fig.suptitle(f'{self.title} Time={time_stamp}')
        self.ax1 = self.fig.subplots(1, 1)

        #  show distribution
        for item in  self.series:
            self.ax1.plot(item['X'], item['Y'])
            #self.ax1.stem(item['TX'], item['TY'])

        if self.уscale_log:
            self.ax1.set_yscale('log')

        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=1, column=1, sticky=tk.N + tk.S + tk.E + tk.W)
        #toobar = NavigationToolbar2Tk(self.canvas, frame)
        tb = VerticalNavigationToolbar2Tk(self.canvas, self)
        tb.update()
        tb.grid(row=1, column=0, sticky=tk.N)    
        self.columnconfigure(1, weight=1)
        #self.rowconfigure(0, weight=1)        
        self.rowconfigure(1, weight=1)

    def make_toolbar(self):
        frame = ttk.Frame(self)
  
        self.chk_var = tk.IntVar(master = self, value=self.уscale_log)
        self.norm_vt_var = tk.IntVar(master = self, value=self.norm_vt_flag)
        self.eng_scale_var = tk.IntVar(master = self, value=self.energy_scale)
        self.diff_var = tk.IntVar(master = self, value=self.energy_scale)
  
        self.checkbtn = ttk.Checkbutton(master=  frame, text="Log scale", variable=self.chk_var, command=self.checkbtn_changed )
        self.checkbtn.pack(side=tk.LEFT,  fill=tk.X, padx=2) 
        vt_btn = ttk.Checkbutton(master=  frame, text="VT norm", variable=self.norm_vt_var, command=self.checkbtn_changed2 )
        vt_btn.pack(side=tk.LEFT,  fill=tk.X, padx=2) 
        eng_btn = ttk.Checkbutton(master=  frame, text="Engery", variable=self.eng_scale_var, command=self.checkbtn_changed2 )
        eng_btn.pack(side=tk.LEFT,  fill=tk.X, padx=2) 
        diff_btn = ttk.Checkbutton(master=  frame, text="Diff", variable=self.diff_var, command=self.checkbtn_changed2 )
        diff_btn.pack(side=tk.LEFT,  fill=tk.X, padx=2) 
        ns= len(self.series)
        self.index_1 = tk.IntVar(master = self, value=0)
        self.index_1.trace_add('write', self.update_plot)
        self.slider_1 = tk.Scale(master=  frame, variable = self.index_1, orient = tk.HORIZONTAL, 
                                    sliderlength = 20,
                                    width = 10,            
                                    label='index',
                                    tickinterval= ns/4,
                                    from_=0, 
                                    to=ns-1, 
                                    resolution=1 )
        self.slider_1.pack(side=tk.LEFT, expand=1, fill=tk.X, padx=5) 

        self.index_2 = tk.IntVar(master = self, value=ns)
        self.index_2.trace_add('write', self.update_plot)
        self.slider_2 = tk.Scale(master=  frame, variable = self.index_2, orient = tk.HORIZONTAL,
                                    sliderlength = 20,
                                    width = 10,            
                                    label='numbers',
                                    tickinterval= ns/4,
                                    from_=1, 
                                    to=ns, 
                                    resolution=1 )
        self.slider_2.pack(side=tk.LEFT, expand=1, fill=tk.X, padx=5)   
            
        return frame
        
    def checkbtn_changed(self):
        if self.chk_var.get() == 1:
            self.уscale_log = True
        else:
            self.уscale_log = False

        self.show_series(save_lim = False) 

    def checkbtn_changed2(self):
        self.norm_vt_flag = True if self.norm_vt_var.get() ==1 else False
        self.energy_scale = True if self.eng_scale_var.get() ==1 else False
        self.diff = True if self.diff_var.get() ==1 else False
        self.series = renorm_series(self.my_series, self.norm_vt_flag, self.energy_scale, self.diff)
        self.show_series(save_lim = False) 

    def update_plot(self, var, indx, mode):
        self.show_series()

    def update(self, m_series, time_stamp):
        self.my_series = m_series
        self.series = renorm_series(m_series, self.norm_vt_flag, self.energy_scale, self.diff)
        self.fig.suptitle(f'{self.title}. Time={time_stamp}')
        self.show_series()

    def show_series(self, save_lim = True):
        if save_lim:
            bottom, top = self.ax1.get_ylim()
            left, right = self.ax1.get_xlim()        
        self.ax1.clear()
        i1 = self.index_1.get()
        i2 = i1 + self.index_2.get()
        if i2>len(self.series):
            i2 = len(self.series)
        print(f'{i1} {i2}')
        for item in self.series[i1:i2]:
            self.ax1.plot(item['X'], item['Y']);
        if self.уscale_log:
            self.ax1.set_yscale('log')
        if save_lim:
            self.ax1.set_ylim(bottom, top)
            self.ax1.set_xlim(left, right)            
        self.canvas.draw()

    def destroy(self):
        if self.fig:
            plt.close(self.fig)
        super().destroy()                   