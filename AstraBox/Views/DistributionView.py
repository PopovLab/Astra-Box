from cgitb import enable
import tkinter as tk
import tkinter.ttk as ttk

from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import ( FigureCanvasTkAgg, NavigationToolbar2Tk)

import AstraBox.Models.ModelFactory as ModelFactory

from AstraBox.Views.HeaderPanel import HeaderPanel
from AstraBox.Views.ExtraRaceView import ExtraRaceView

class DistributionView(ttk.Frame):
    def __init__(self, master, model) -> None:
        super().__init__(master)  
        self.model = model
        self.distribution_list = model.get_distribution_list()
        n = len(self.distribution_list)
        if n>0: 
            distribution, self.start_time  =  self.get_distribution(0)
            _, self.finish_time  = self.get_distribution(n-1)
            self.n = n

            self.time_var = tk.DoubleVar(master = self, value=self.start_time)
            self.time_var.trace_add('write', self.update_time_var)

            self.time_slider = tk.Scale(master=  self, 
                                   variable = self.time_var,
                                   orient = tk.HORIZONTAL,
                                   label='Time scale',
                                   tickinterval= (self.finish_time-self.start_time)/7,
                                   from_= self.start_time,
                                   to= self.finish_time, 
                                   resolution= (self.finish_time-self.start_time)/n, 
                                   length = 250 )
            self.time_slider.grid(row=1, column=0, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W)       
            
            self.plot = DistributionPlot(self, distribution, self.start_time)
            self.plot.grid(row=2, column=0, sticky=tk.W, pady=4, padx=8)

    def get_distribution(self, index):
        file = self.distribution_list[index]
        print(f'{file} {index}')
        return self.model.read_distribution(file)

    def update_time_var(self, var, indx, mode):
        index = int((self.n-1) * (self.time_var.get()-self.start_time) / (self.finish_time-self.start_time))
        distribution, time_stamp = self.get_distribution(index)
        self.plot.update(distribution, time_stamp)

    def update_var(self, var, indx, mode):
        distribution, time_stamp  = self.get_distribution(self.index_var.get())
        self.plot.update(distribution)

class DistributionPlot(ttk.Frame):
    def __init__(self, master, distribution, time_stamp) -> None:
        super().__init__(master)  
        #self.fig, self.axs = plt.subplots(2, 2, figsize=(7, 6))
        self.fig = plt.figure(figsize=(8, 5))
        self.fig.suptitle(f'Distribution. Time={time_stamp}')
        self.ax1 = self.fig.subplots(1, 1)
        
        # 
        for line in distribution:
            #self.ax1.plot(line['X'], line['Y'])
            self.ax1.plot(line['X'], line['logY']);


        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=1, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        frame = ttk.Frame(self)
        frame.grid(row=0, column=0, sticky=tk.W)
        toobar = NavigationToolbar2Tk(self.canvas, frame)
        #tb = VerticalNavigationToolbar2Tk(canvas, frame)
        #canvas.get_tk_widget().grid(row=2, column=0)

    def update(self, distribution, time_stamp):
        self.fig.suptitle(f'Distribution. Time={time_stamp}')
        self.ax1.clear()
        for line in distribution:
            #self.ax1.plot(line['X'], line['Y'])
            self.ax1.plot(line['X'], line['logY']);

        self.ax1.set_ylim(-30, 0)
        #self.ax1.autoscale_view(True,True,True)        

        self.canvas.draw()

    def destroy(self):
        print("DistributionPlot destroy")
        if self.fig:
            plt.close(self.fig)
        super().destroy()   