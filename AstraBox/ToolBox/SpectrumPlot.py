from enum import auto
import os
from pathlib import Path
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog 
import numpy as np
from matplotlib import cm
import pandas as pd

import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg') 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk



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
        X, Y, Z = spectrum['Ntor'], spectrum['Npol'], spectrum['Amp']

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

class Navigator(VerticalNavigationToolbar2Tk):
    def __init__(self, canvas, window):
        super().__init__(canvas, window)
        self.on_cross = None
      
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
        ax1.plot(spectrum['Ntor'], spectrum['Amp'])
        ax2 = self.fig.add_subplot(gs[1, 1])
        ax2.plot(spectrum['Npol'], spectrum['Amp'])
        # spans two rows:
        #ax = self.fig.add_subplot(gs[:, 0], projection='3d')
        ax_2D = self.fig.add_subplot(gs[:, 0])
        cmhot = plt.get_cmap("plasma")
        area = [3] * len(spectrum['Npol'])
        ax_2D.scatter(spectrum['Ntor'], spectrum['Npol'], s = area, c = spectrum['Amp'],  cmap=cmhot) #, c=c, marker=m)

        ax_2D.set_xlabel('Ntor')
        ax_2D.set_ylabel('Npol')
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

def filter_spectrum(s, level):
    tuple_list = [(t, p, a) for t, p, a in zip(s['Ntor'], s['Npol'], s['Amp'])]
    sort_list = list(filter(lambda x: x[2]> level, tuple_list))
    out = {}
    out['Ntor'] = [x[0] for x in sort_list]
    out['Npol'] = [x[1] for x in sort_list]
    out['Amp']  = [x[2] for x in sort_list]
    return out

def sort_spectrum(s):
    tuple_list = [(t, p, a) for t, p, a in zip(s['Ntor'], s['Npol'], s['Amp'])]
    sort_list = sorted(tuple_list, key=lambda x: x[2])
    out = {}
    out['Ntor'] = [x[0] for x in sort_list]
    out['Npol'] = [x[1] for x in sort_list]
    out['Amp']  = [x[2] for x in sort_list]
    return out


class ScatterPlot2D3D(ttk.Frame):
    def __init__(self, master, spectr) -> None:
        super().__init__(master)  
        spectrum = sort_spectrum(spectr)
        self.sorted_spectrum = spectrum

        self.z_min, self.z_max = MinMax(spectrum['Ntor'])
        self.y_min, self.y_max = MinMax(spectrum['Npol'])        
        self.fig = plt.figure(figsize=(10, 4.3), dpi=100)        
        gs = self.fig.add_gridspec(1, 2)

        ax_2D = self.fig.add_subplot(gs[0, 0])
        cmhot = plt.get_cmap("plasma")
        area = [5] * len(spectrum['Npol'])
        self.scatter= ax_2D.scatter(spectrum['Ntor'], spectrum['Npol'], s = area, c = spectrum['Amp'],  cmap=cmhot, alpha=0.8) #, c=c, marker=m)

        ax_2D.set_xlabel('Ntor')
        ax_2D.set_ylabel('Npol')
        #ax.set_zlabel('Px')

        ax_3D = self.fig.add_subplot(gs[0, 1], projection='3d')
        cmhot = plt.get_cmap("plasma")
        self.scatter3D= ax_3D.scatter(spectrum['Ntor'], spectrum['Npol'], spectrum['Amp'],c = spectrum['Amp'], cmap=cmhot) #, c=c, marker=m)

        ax_3D.set_xlabel('Ntor')
        ax_3D.set_ylabel('Npol')
        ax_3D.set_zlabel('Px') # type: ignore

        self.canvas = FigureCanvasTkAgg(self.fig, self)   
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=1, sticky=tk.N + tk.S + tk.E + tk.W)
        tb = VerticalNavigationToolbar2Tk(self.canvas, self)
        tb.update()
        tb.grid(row=0, column=0, sticky=tk.N)       
        
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1) 

    def save_file(self, cut_level:float):
        fs = filter_spectrum(self.sorted_spectrum, cut_level)
        file_object = filedialog.asksaveasfile(
            mode='w', # 'w' для записи, 'wb' для бинарного
            defaultextension=".dat", # Расширение по умолчанию
            filetypes=[("Text files", "*.dat"), ("All files", "*.*")] # Типы файлов
        )
        if file_object:
            for Ntor, Npol, Amp in zip(fs['Ntor'],fs['Npol'],fs['Amp']):
                line = f"{Ntor:.6f} {Npol:.6f} {Amp:.6f}\n"
                file_object.write(line)
        else:
            print("Сохранение отменено")

    def update_level(self, cut_level:float):
        fs = filter_spectrum(self.sorted_spectrum , cut_level)
        new_offsets = np.vstack((fs['Ntor'], fs['Npol'])).T
        self.scatter.set_offsets(new_offsets)
        self.scatter.set_array(fs['Amp'])
        self.canvas.draw()
        return len(fs['Ntor'])

    def destroy(self):
        print("ScatterPlot3D destroy")
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
        ax1.plot(spectrum['Ntor'], spectrum['Amp'])
        ax2 = self.fig.add_subplot(gs[1, 1])
        ax2.plot(spectrum['Npol'], spectrum['Amp'])
        # spans two rows:
        ax_3D = self.fig.add_subplot(gs[:, 0], projection='3d')
        cmhot = plt.get_cmap("plasma")
        ax_3D.scatter(spectrum['Ntor'], spectrum['Npol'], spectrum['Amp'],c = spectrum['Amp'], cmap=cmhot) #, c=c, marker=m)

        ax_3D.set_xlabel('Ntor')
        ax_3D.set_ylabel('Npol')
        ax_3D.set_zlabel('Px')

        self.canvas = FigureCanvasTkAgg(self.fig, self)   
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=1, sticky=tk.N + tk.S + tk.E + tk.W)
        tb = VerticalNavigationToolbar2Tk(self.canvas, self)
        tb.update()
        tb.grid(row=0, column=0, sticky=tk.N)      
  
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1) 


    def destroy(self):
        print("ScatterPlot3D destroy")
        if self.fig:
            plt.close(self.fig)
        super().destroy()   

import numpy.ma as ma

def downsample_with_max_mask(data, window_size, factor):
    """
    Downsampling 2D массива с сохранением всех точек с максимальным значением в окне.
    
    Parameters:
    -----------
    data : numpy.ndarray
        2D входной массив
    window_size : int
        Размер окна для downsampling (окно квадратное window_size x window_size)
    
    Returns:
    --------
    mask : numpy.ndarray
        Маска того же размера, что и входной массив, где True - точки, которые сохраняются
    """
    if len(data.shape) != 2:
        raise ValueError("Input data must be 2D array")
    
    if window_size <= 0:
        raise ValueError("Window size must be positive")
    
    print('downsample_with_max_mask', data.shape)
    h, w = data.shape

    mask = np.full_like(data, fill_value=True, dtype=bool)
    
    # Проходим по всем окнам
    for i in range(0, h, window_size):
        for j in range(0, w, window_size):
            # Определяем границы текущего окна
            i_end = min(i + window_size, h)
            j_end = min(j + window_size, w)
            
            # Получаем текущее окно
            window = data[i:i_end, j:j_end]
            
            if window.size > 0:  # Проверяем, что окно не пустое
                # Находим максимальное значение в окне
                #level = np.mean(window)
                max_v = np.max(window)
                min_v = np.min(window)
                level = factor*(max_v-min_v) + min_v
                # Создаем локальную маску для окна
                local_mask = (window > level)
                
                # Переносим локальную маску в общую маску
                mask[i:i_end, j:j_end][local_mask] = False
    
    return mask

def apply_filter(data, filter):
    match filter['window']:
        case 'none': pass
        case '[2x2]':
            mask = downsample_with_max_mask(data, 2, filter['factor'])
            data = ma.masked_array(data, mask= mask)
        case '[3x3]':
            mask = downsample_with_max_mask(data, 3, filter['factor'])
            data = ma.masked_array(data, mask= mask)
        case '[5x5]':
            mask = downsample_with_max_mask(data, 5, filter['factor'])
            data = ma.masked_array(data, mask= mask)                
    masked_data = ma.masked_where((data < filter['threshold']), data)
    return masked_data

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
        self.image= axd['left'].imshow(spectrum['Amp'], origin='lower', extent=[self.z_min, self.z_max, self.y_min, self.y_max])
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
        self.canvas.get_tk_widget().grid(row=0, column=1)
        toobar = Navigator(self.canvas, self)        
        toobar.on_cross = self.on_cross
        toobar.grid(row=0, column=0, sticky=tk.W)
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
        Y = self.spectrum['Amp'][::-1, col]
        return X, Y

    def get_row(self, row):
        X = self.spectrum['Nz'][row]
        Y = self.spectrum['Amp'][row]
        return X, Y
       
    def apply_filter(self, filter):
        masked_data = apply_filter(self.spectrum['Amp'], filter)
        self.image.set_data(masked_data)
        self.canvas.draw()
        return masked_data.count()

    def export_to_file(self, filter):
        masked_data = apply_filter(self.spectrum['Amp'], filter)
        # Запись только незамаскированных значений
        Nz_coords = self.spectrum['Nz']
        Ny_coords = self.spectrum['Ny']
        file_object = filedialog.asksaveasfile(
            mode='w', # 'w' для записи, 'wb' для бинарного
            defaultextension=".dat", # Расширение по умолчанию
            filetypes=[("Text files", "*.dat"), ("All files", "*.*")] # Типы файлов
        )
        if file_object:
            #file.write("# Nz Ny Amp")
            for i in range(self.spectrum_shape[0]):
                for j in range(self.spectrum_shape[1]):
                    if not masked_data.mask[i, j]:  # Проверяем, не замаскировано ли значение
                        line = f"{Nz_coords[i, j]:.6f} {Ny_coords[i,j]:.6f} {masked_data[i, j]:.6f}\n"
                        file_object.write(line)
        else:
            print("Сохранение отменено")

    def destroy(self):
        print("Plot2D destroy")
        if self.fig:
            plt.close(self.fig)
        super().destroy()   

class SpectrumPlot(ttk.Frame):
    def __init__(self, master, X= None, Y= None, spectrum_list = None) -> None:
        super().__init__(master)  
        self.fig = plt.figure(figsize=(5, 3), dpi=100)
        self.ax = self.fig.add_subplot(111)
        if spectrum_list:
            for sp in spectrum_list:
                if sp is not None:
                    self.ax.plot(sp['Ntor'], sp['Amp'])    
        else:
            self.ax.plot(X, Y)
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=1, sticky=tk.N + tk.S + tk.E + tk.W)
        #toobar = NavigationToolbar2Tk(canvas, frame)
        tb = VerticalNavigationToolbar2Tk(self.canvas, self)
        tb.update()
        tb.grid(row=0, column=0, sticky=tk.N)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)        

    def add_compare_spectrum(self, X= None, Y= None):
        self.ax.plot(X, Y)
        self.canvas.draw()

    def destroy(self):
        print("SpectrumPlot destroy")
        if self.fig:
            plt.close(self.fig)
        super().destroy()       

class RotatedSpectrumPlot(ttk.Frame):
    def __init__(self, master, X= None, Y= None, V = None) -> None:
        super().__init__(master)  
        #self.fig = plt.figure(figsize=(5, 3), dpi=100)
        #ax = self.fig.add_subplot(111)
        self.fig, axs = plt.subplots(2, 2, layout='constrained')
        axs[0,0].plot(X, V)
        axs[0,0].set_xlabel('N tor')
        axs[0,1].plot(Y, V)
        axs[0,1].set_xlabel('N pol')
        axs[1,0].scatter(X, Y, c=V, cmap='RdBu_r')
        axs[1,0].set_ylabel('N pol')
        axs[1,0].set_xlabel('N tor')
        axs[1,0].axis('equal')

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

def cumtrapz(x,y):
    # аналог scipy.integrate.cumtrapz
    # что бы не подключать scipy
    y1 = np.roll(y, -1)
    x1 = np.roll(x, -1)
    xy= (y+y1)*(x1-x)/2
    r = np.cumsum(xy)
    print(type(r))
    if type(r) == pd.Series:
        r.iloc[-1] = r.iloc[-2]
    else: # numpy.ndarray
        r[-1] = r.take(-2)
    return r


class SpectrumChart(ttk.Frame):
    def __init__(self, master, spectrums: dict, nteta:int, show_summary:bool=True) -> None:
        super().__init__(master)  

        self.spectrums = spectrums
        self.nteta = nteta
        p = self.make_check_panel()
        p.grid(row=0, column=2, sticky=tk.N)

        self.fig = plt.figure(figsize=(5, 3), dpi=100)
        self.ax = self.fig.add_subplot(111)


        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.make_plots()
        
        self.canvas.get_tk_widget().grid(row=0, column=1, sticky=tk.N + tk.S + tk.E + tk.W)
        #toobar = NavigationToolbar2Tk(canvas, frame)
        tb = VerticalNavigationToolbar2Tk(self.canvas, self)
        tb.update()
        tb.grid(row=0, column=0, sticky=tk.N)

        if show_summary:
            txt = self.make_summary()
            txt.grid(row=1, column=1, padx=4, pady=4, sticky=tk.N + tk.S + tk.E + tk.W)
        
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

    def make_summary(self):
        xsgs = 1e+13 # 1MW = 1e13 erg/s ( 1 mega watts)
        text_box = tk.Text(self, height = 15, width = 50)
        lines = [f'nteta: {self.nteta}']
        indent = ' '
        for key, s in self.spectrums.items():
            if s is not None:
                p = np.sum(s["Amp"])
                #p = np.trapz(s["Amp"], s['Ntor'])
                r = s['trapz']
                if type(r) == pd.Series:
                    p2 = r.iloc[-1]
                    size = r.size
                    v = s['Ntor'].iloc[-1]
                else: # numpy.ndarray
                    p2 = r[-1]
                    size = len(r)
                    v = s['Ntor'][-1]
                l = len(key)
                lines.append(indent + f'{key}: {p} ')
                #lines.append(indent + f'{key}: {p2} ')
                lines.append(indent + " "*(l-4)  +'beam' + f': {p/xsgs:.4f} MW')
                #lines.append(indent + " "*(l-4)  +'beam' + f': {p2/xsgs:.4f} MW')
                lines.append(indent + " "*(l-5)  +'total' + f': {self.nteta*p/xsgs:.4f} MW ')
                lines.append(indent + " "*(l-4)  +'size' + f': {size} ')
                
        text_box.insert(tk.END, '\n'.join(lines))
        text_box.config(state='disabled')
        return text_box

    def make_plots(self):
        self.ax.clear()
        for key, s in self.spectrums.items():
            if s is not None:
                if self.check_vars[key].get() == 1:
                    print(key)
                    #kwargs = 
                    marker=None if len(s['Ntor']) >300 else '|'
                    
                    match self.spectrum_view.get():
                        case 'spectrum':
                            self.ax.plot(s['Ntor'], s['Amp'], marker= marker)
                        case 'cumsum':
                            self.ax.plot(s['Ntor'], np.cumsum(s['Amp']), marker= marker)
                        case 'integral':
                            self.ax.plot(s['Ntor'], s['trapz'], marker= marker)
                        
        self.canvas.draw()

    def make_check_panel(self):
        panel = tk.Frame(self)
        self.spectrum_view = tk.StringVar(value='spectrum') 
        btn1 = ttk.Radiobutton(panel, text='spectrum', value= 'spectrum', variable=self.spectrum_view, command=self.checkbutton_changed)
        btn1.pack(padx=6, pady=6, anchor=tk.NW)

        btn2 = ttk.Radiobutton(panel, text='cumsum', value= 'cumsum', variable=self.spectrum_view, command=self.checkbutton_changed)
        btn2.pack(padx=6, pady=6, anchor=tk.NW)

        btn3 = ttk.Radiobutton(panel, text='integral', value= 'integral', variable=self.spectrum_view, command=self.checkbutton_changed)
        btn3.pack(padx=6, pady=6, anchor=tk.NW)

        sep = ttk.Separator(panel,orient='horizontal')
        sep.pack(padx=6, pady=6, fill='x')

        self.check_vars = {}
        for key, s in self.spectrums.items():
            if s is not None:
                v = tk.IntVar(value=1)
                b = ttk.Checkbutton(panel, text=key, variable=v, command=self.checkbutton_changed)
                b.pack(padx=6, pady=6, anchor=tk.NW)
                self.check_vars[key] = v
                print(f'--- {key} ----')
                s['trapz'] = cumtrapz(s['Ntor'], s['Amp'])
        return panel
    
    def checkbutton_changed(self):
        for key, s in self.spectrums.items():
            if s is not None:
                print(f'{key} {self.check_vars[key].get()}')
        print(f'spectrum_view: {self.spectrum_view.get()}')
        self.make_plots()

    def destroy(self):
        print("SpectrumPlot destroy")
        if self.fig:
            plt.close(self.fig)
        super().destroy()       