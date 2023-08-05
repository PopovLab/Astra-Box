import tkinter as tk
import tkinter.ttk as ttk

from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import ( FigureCanvasTkAgg, NavigationToolbar2Tk)
from AstraBox.ToolBox.VerticalNavigationToolbar import VerticalNavigationToolbar2Tk


#variable name
class RTResultPlot(ttk.Frame):
    def __init__(self, master, rt_result_dict, keys) -> None:
        super().__init__(master)  

        self.rt_result_dict = rt_result_dict
        self.fig = plt.figure(figsize=(8, 6), dpi=100)

        gs = self.fig.add_gridspec(2, 1)
        ax1 = self.fig.add_subplot(gs[0, 0])
        #  show rt result in View 1
        self.plot_data(ax1, keys[0], 1)
        self.plot_data(ax1, keys[0], -1)

        ax2 = self.fig.add_subplot(gs[1, 0])
        #  show rt result in View 2
        self.plot_data(ax2, keys[1], 1)
        self.plot_data(ax2, keys[1], -1)
        
        ax1.set_ylabel(keys[0])
        ax2.set_ylabel(keys[1])
        ax2.set_xlabel('Time')

        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=1, sticky=tk.N + tk.S + tk.E + tk.W)
        #toobar = NavigationToolbar2Tk(self.canvas, frame)
        tb = VerticalNavigationToolbar2Tk(self.canvas, self)
        tb.update()
        tb.grid(row=0, column=0, sticky=tk.N)    
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)    

    def plot_data(self, axis, variable_name, direction):
        color = 'red' if direction>0 else 'blue'
        legend = 'pos' if direction>0 else 'neg'
        
        X = []
        Y = []
        X0 = []
        Y0 = []
        for time_stamp, rt_result in self.rt_result_dict.items():
            iteration = 0
            for key, values in rt_result[direction].items():
                if key > iteration: iteration= key
                X.append(time_stamp)
                Y.append(values[variable_name])
            if iteration == 0: continue
            values = rt_result[direction][iteration]
            X0.append(time_stamp)
            Y0.append(values[variable_name])
        area = [3] * len(X)
        axis.scatter(X, Y, s=area, c= color)
        axis.plot(X0, Y0, c= color, label= legend)
        axis.legend(loc='upper right')

    def destroy(self):
        if self.fig:
            plt.close(self.fig)
        super().destroy()  