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
        variable_name = keys[0]
        #self.fig, self.axs = plt.subplots(2, 2, figsize=(7, 6))
        self.rt_result_dict = rt_result_dict
        self.fig = plt.figure(figsize=(8, 5))
        self.fig.suptitle(f'RT Result. {variable_name}')
        self.ax1 = self.fig.subplots(1, 1)
        
        #  show rt result
        self.plot_data(variable_name, 1)
        self.plot_data(variable_name, -1)

        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=1, sticky=tk.N + tk.S + tk.E + tk.W)
        #toobar = NavigationToolbar2Tk(self.canvas, frame)
        tb = VerticalNavigationToolbar2Tk(self.canvas, self)
        tb.update()
        tb.grid(row=0, column=0, sticky=tk.N)    
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)    

    def plot_data(self, variable_name, direction):
        color = 'red'
        if direction>0: color = 'blue'
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
            values = rt_result[direction][iteration]
            X0.append(time_stamp)
            Y0.append(values[variable_name])
        area = [3] * len(X)
        self.ax1.scatter(X, Y, s=area, c= color)
        self.ax1.plot(X0, Y0, c= color)

    def destroy(self):
        if self.fig:
            plt.close(self.fig)
        super().destroy()  