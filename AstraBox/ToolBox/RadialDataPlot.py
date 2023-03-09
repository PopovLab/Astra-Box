import tkinter as tk
import tkinter.ttk as ttk

from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import ( FigureCanvasTkAgg, NavigationToolbar2Tk)
from AstraBox.ToolBox.VerticalNavigationToolbar import VerticalNavigationToolbar2Tk


class RadialDataPlot(ttk.Frame):
    def __init__(self, master, profiles) -> None:
        super().__init__(master)  
        #self.fig, self.axs = plt.subplots(2, 2, figsize=(7, 6))
        self.fig = plt.figure(figsize=(8, 6.6))
        self.fig.suptitle(f'Astra radial data. Time={profiles["Time"]}')
        self.axs = self.fig.subplots(2, 2)
        
        # профили токов
        self.profile_J,    = self.axs[0,0].plot(profiles['a'], profiles['J'], label='J')
        self.profile_Johm, = self.axs[0,0].plot(profiles['a'], profiles['Johm'], label='Johm')
        self.profile_Jlh, = self.axs[0,0].plot(profiles['a'], profiles['Jlh'], label='Jlh')
        #self.axs[0,0].set_title("J, Johm, Jlh")
        self.axs[0,0].legend(loc='upper right', shadow=True)

        # профили E
        self.profile_E, = self.axs[0,1].plot(profiles['a'], profiles['E'], label='E')
        self.profile_En, = self.axs[0,1].plot(profiles['a'], profiles['En'], label='En')
        #self.axs[0,1].set_title("E, En")
        self.axs[0,1].legend(loc='upper right', shadow=True)
    
        # профили мощности
        self.profile_Plh, = self.axs[1,0].plot(profiles['a'], profiles['Plh'], label='Plh')
        self.profile_Poh, = self.axs[1,0].plot(profiles['a'], profiles['Poh'], label='Poh')
        #self.axs[1,0].set_title("Plh, Poh")
        self.axs[1,0].legend(loc='upper right', shadow=True)
    
        # профили температуры
        self.profile_Te, = self.axs[1,1].plot(profiles['a'], profiles['Te'], label='Te')
        #self.profile_Poh, = self.axs[2].plot(profiles['Poh'])
        #self.axs[1,1].set_title("Te")
        self.axs[1,1].legend(loc='upper right', shadow=True)

        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=1, sticky=tk.N + tk.S + tk.E + tk.W)

        #toobar = NavigationToolbar2Tk(self.canvas, frame)
        tb = VerticalNavigationToolbar2Tk(self.canvas, self)
        tb.update()
        tb.grid(row=0, column=0, sticky=tk.N)        
        
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

    def update(self, profiles):
        self.fig.suptitle(f'Astra radial data. Time={profiles["Time"]}')

        self.profile_J.set_ydata(profiles['J']) 
        self.profile_Johm.set_ydata(profiles['Johm']) 
        self.profile_Jlh.set_ydata(profiles['Jlh']) 
        self.axs[0,0].relim()
        self.axs[0,0].autoscale_view(True,True,True)        

        self.profile_E.set_ydata(profiles['E']) 
        self.profile_En.set_ydata(profiles['En']) 
        self.axs[0,1].relim()
        self.axs[0,1].autoscale_view(True,True,True) 

        self.profile_Plh.set_ydata(profiles['Plh']) 
        self.profile_Poh.set_ydata(profiles['Poh']) 
        self.axs[1,0].relim()
        self.axs[1,0].autoscale_view(True,True,True) 
        
        self.profile_Te.set_ydata(profiles['Te']) 
        self.axs[1,1].relim()
        self.axs[1,1].autoscale_view(True,True,True)         

        self.canvas.draw()

    def destroy(self):
        if self.fig:
            plt.close(self.fig)
        super().destroy()   
