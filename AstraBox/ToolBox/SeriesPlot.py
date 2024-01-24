import tkinter as tk
import tkinter.ttk as ttk

from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import ( FigureCanvasTkAgg, NavigationToolbar2Tk)
from AstraBox.ToolBox.VerticalNavigationToolbar import VerticalNavigationToolbar2Tk


def renorm_vel(maxwell):
    X = maxwell['X']
    Y = maxwell['Y']
    vmax = abs(X[0])
    X = 2* X / vmax
    #Y = Y * vmax /1000 #Эмпирический коэффициент
    #print(np.sum(Y))
    print('renorm')
    XX = []
    YY = []
    for xv, yv in zip(X,Y):
        if abs(xv)<=1:
            XX.append(xv)
            YY.append(yv)

    return {'X': XX, 'Y': YY}

def renorm_series(series):
    new_series = []
    for item in series:
        new_series.append(renorm_vel(item))
    return new_series

class SeriesPlot(ttk.Frame):
    def __init__(self, master, series, title, time_stamp, уscale_log = True) -> None:
        super().__init__(master)  
        print('SeriesPlot')
        self.уscale_log = уscale_log
        self.title = title
        self.series = renorm_series(series)

        tb = self.make_toolbar()
        tb.grid(row=0, column=0, columnspan=2, sticky=tk.N + tk.S + tk.E + tk.W) 

        self.fig = plt.figure(figsize=(8, 5))
        self.fig.suptitle(f'{self.title} Time={time_stamp}')
        self.ax1 = self.fig.subplots(1, 1)

        #  show distribution
        for item in self.series:
            self.ax1.plot(item['X'], item['Y']);

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
  
        self.checkbtn = ttk.Checkbutton(master=  frame, text="Log scale", variable=self.chk_var, command=self.checkbtn_changed )
        self.checkbtn.pack(side=tk.LEFT, expand=1, fill=tk.X, padx=5) 
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

    def update_plot(self, var, indx, mode):
        self.show_series()

    def update(self, series, time_stamp):
        self.series =  renorm_series(series)
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