from enum import auto
import os
import tkinter as tk
import tkinter.ttk as ttk
import numpy as np
from matplotlib import cm

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import ( FigureCanvasTkAgg, NavigationToolbar2Tk)


class VerticalNavigationToolbar2Tk(NavigationToolbar2Tk):
   def __init__(self, canvas, window):
      super().__init__(canvas, window, pack_toolbar=False)

   # override _Button() to re-pack the toolbar button in vertical direction
   def _Button(self, text, image_file, toggle, command):
      b = super()._Button(text, image_file, toggle, command)
      b.pack(side=tk.TOP) # re-pack button in vertical direction
      return b

   # override _Spacer() to create vertical separator
   def _Spacer(self):
      s = tk.Frame(self, width=26, relief=tk.RIDGE, bg="DarkGray", padx=2)
      s.pack(side=tk.TOP, pady=5) # pack in vertical direction
      return s

   # disable showing mouse position in toolbar
   def set_message(self, s):
      pass

class Plot3D(ttk.Frame):
    def __init__(self, master, spectrum) -> None:
        super().__init__(master)
        self.fig = plt.figure(figsize=(5,5))
        ax = self.fig.add_subplot(projection='3d')
        X, Y, Z = spectrum['Ntor'], spectrum['Npol'], spectrum['Px']

        # Plot the 3D surface
        #ax.plot_surface(X, Y, Z, rstride=8, cstride=8, alpha=0.5)
        ax.plot_surface(X, Y, Z, alpha=0.5)
        # Plot projections of the contours for each dimension.  By choosing offsets
        # that match the appropriate axes limits, the projected contours will sit on
        # the 'walls' of the graph
        ax.contourf(X, Y, Z, zdir='z', offset=-0.1, cmap=cm.coolwarm, alpha=0.8)
        ax.contourf(X, Y, Z, zdir='x', offset=-10, cmap=cm.coolwarm)
        ax.contourf(X, Y, Z, zdir='y', offset=10, cmap=cm.coolwarm)

        ax.set(xlim=(-10, 10), ylim=(-10, 10), zlim=(-0.1, 1.5),
            xlabel='X', ylabel='Y', zlabel='Z')

        canvas = FigureCanvasTkAgg(self.fig, self)   
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=0)
        frame = ttk.Frame(self)
        frame.grid(row=0, column=0, sticky=tk.W)
        toobar = NavigationToolbar2Tk(canvas, frame)   

    def destroy(self):
        print("Plot2D destroy")
        if self.fig:
            plt.close(self.fig)
        super().destroy()   

class Navigator(NavigationToolbar2Tk):
    on_cross = None
    def mouse_move(self, event):
        #self._set_cursor(event)
        if event.button == None: return
        if event.inaxes and event.inaxes.get_navigate():
            try:
                s = event.inaxes.format_coord(event.xdata, event.ydata)
                print(s)
                if self.on_cross:
                    self.on_cross(event.xdata, event.ydata)
                self.set_message(s)
            except (ValueError, OverflowError):
                pass
        else:
            self.set_message(self.mode)

def MinMax(arr):
    return np.amin(arr), np.amax(arr)

class ScatterPlot(ttk.Frame):
    def __init__(self, master, spectrum) -> None:
        super().__init__(master)  
        self.spectrum = spectrum
        self.z_min, self.z_max = MinMax(self.spectrum['Ntor'])
        self.y_min, self.y_max = MinMax(self.spectrum['Npol'])        
        self.fig = plt.figure(figsize=(10, 4.3), dpi=100)        
        gs = self.fig.add_gridspec(2, 2)
        ax1 = self.fig.add_subplot(gs[0, 1])
        ax1.plot(spectrum['Ntor'], spectrum['Px'])
        ax2 = self.fig.add_subplot(gs[1, 1])
        ax2.plot(spectrum['Npol'], spectrum['Px'])
        # spans two rows:
        #ax = self.fig.add_subplot(gs[:, 0], projection='3d')
        ax = self.fig.add_subplot(gs[:, 0])
        cmhot = plt.get_cmap("plasma")
        area = [3] * len(spectrum['Npol'])
        ax.scatter(spectrum['Ntor'], spectrum['Npol'], s = area, c = spectrum['Px'],  cmap=cmhot) #, c=c, marker=m)

        ax.set_xlabel('Ntor')
        ax.set_ylabel('Npol')
        #ax.set_zlabel('Px')

        self.canvas = FigureCanvasTkAgg(self.fig, self)   
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=1)
        tb = VerticalNavigationToolbar2Tk(self.canvas, self)
        tb.update()
        tb.grid(row=0, column=0, sticky=tk.N)        

    def destroy(self):
        print("ScatterPlot destroy")
        if self.fig:
            plt.close(self.fig)
        super().destroy()   


class ScatterPlot3D(ttk.Frame):
    def __init__(self, master, spectrum) -> None:
        super().__init__(master)  
        self.spectrum = spectrum
        self.z_min, self.z_max = MinMax(self.spectrum['Ntor'])
        self.y_min, self.y_max = MinMax(self.spectrum['Npol'])        
        self.fig = plt.figure(figsize=(10, 4.3), dpi=100)        
        gs = self.fig.add_gridspec(2, 2)
        ax1 = self.fig.add_subplot(gs[0, 1])
        ax1.plot(spectrum['Ntor'], spectrum['Px'])
        ax2 = self.fig.add_subplot(gs[1, 1])
        ax2.plot(spectrum['Npol'], spectrum['Px'])
        # spans two rows:
        ax = self.fig.add_subplot(gs[:, 0], projection='3d')
        #ax = self.fig.add_subplot(gs[:, 0])
        cmhot = plt.get_cmap("plasma")
        ax.scatter(spectrum['Ntor'], spectrum['Npol'], spectrum['Px'],c = spectrum['Px'], cmap=cmhot) #, c=c, marker=m)

        ax.set_xlabel('Ntor')
        ax.set_ylabel('Npol')
        ax.set_zlabel('Px')

        self.canvas = FigureCanvasTkAgg(self.fig, self)   
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=1)
        tb = VerticalNavigationToolbar2Tk(self.canvas, self)
        tb.update()
        tb.grid(row=0, column=0, sticky=tk.N)        

    def destroy(self):
        print("ScatterPlot3D destroy")
        if self.fig:
            plt.close(self.fig)
        super().destroy()   


class Plot2DArray(ttk.Frame):
    def __init__(self, master, spectrum) -> None:
        super().__init__(master)  
        self.spectrum = spectrum
        self.fig = plt.figure(figsize=(11, 4.7), dpi=100)
        axd = self.fig.subplot_mosaic([['left', 'upper right'],
                                       ['left', 'lower right']])
        #plt.title("Spectrum")
        #plt.style.use('_mpl-gallery-nogrid')
        self.spectrum_shape = spectrum['Nz'].shape
        print(self.spectrum_shape)
        self.z_min, self.z_max = MinMax(self.spectrum['Nz'][0])
        self.y_min, self.y_max = MinMax(self.spectrum['Ny'][:, 0])
        #X, Y = np.meshgrid(, self.spectrum['Npol'][:, 0])
        #axd['left'].pcolormesh(X, Y, spectrum['Px'], vmin=0.0, vmax=0.5)
        axd['left'].imshow(spectrum['Px'], extent=[self.z_min, self.z_max, self.y_min, self.y_max])
        self.v_cross, = axd['left'].plot([0, 0], [self.z_min+0.1, self.z_max-0.1])
        self.h_cross, = axd['left'].plot([self.y_min, self.y_max], [0, 0])

        X,Y = self.get_row(100)
        self.h_ax = axd['lower right']
        self.h_line, = self.h_ax.plot(X, Y)
        self.v_ax = axd['upper right']
        X,Y = self.get_col(100)
        self.v_line, = self.v_ax.plot(X, Y)        
        self.canvas = FigureCanvasTkAgg(self.fig, self)   
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=1, column=0)
        frame = ttk.Frame(self)
        frame.grid(row=0, column=0, sticky=tk.W)
        toobar = Navigator(self.canvas, frame)        
        toobar.on_cross = self.on_cross
        self.on_cross(0,0)

    def on_cross(self, x,y):
        #print(f"{x}, {y}")       
        self.v_cross.set_xdata([x,x]) 
        self.h_cross.set_ydata([y,y]) 
        ry = self.spectrum_shape[0] *(1 - (y - self.y_min)/(self.y_max-self.y_min))
        rx = self.spectrum_shape[1] *(x - self.z_min)/(self.z_max-self.z_min)
        X,Y = self.get_row(int(ry))
        self.h_line.set_ydata(Y)
        self.h_ax.relim()
        self.h_ax.autoscale_view(True,True,True)

        X,Y = self.get_col(int(rx))
        self.v_line.set_ydata(Y)
        self.v_ax.relim()
        self.v_ax.autoscale_view(True,True,True)        

        self.canvas.draw()


    def get_col(self, col):
        X = self.spectrum['Ny'][:, col]
        Y = self.spectrum['Px'][::-1, col]
        return X, Y

    def get_row(self, row):
        X = self.spectrum['Nz'][row]
        Y = self.spectrum['Px'][row]
        return X, Y


    def destroy(self):
        print("Plot2D destroy")
        if self.fig:
            plt.close(self.fig)
        super().destroy()   

class SpectrumPlot(ttk.Frame):
    def __init__(self, master, X, Y) -> None:
        super().__init__(master)  
        self.fig = plt.figure(figsize=(5, 3), dpi=100)
        self.fig.add_subplot(111).plot(X, Y)
        canvas = FigureCanvasTkAgg(self.fig, self)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=1)
        #toobar = NavigationToolbar2Tk(canvas, frame)
        tb = VerticalNavigationToolbar2Tk(canvas, self)
        tb.update()
        tb.grid(row=0, column=0, sticky=tk.N)

    def destroy(self):
        print("SpectrumPlot destroy")
        if self.fig:
            plt.close(self.fig)
        super().destroy()       