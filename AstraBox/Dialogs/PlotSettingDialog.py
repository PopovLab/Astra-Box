import gc
import json
import tkinter as tk
import tkinter
import tkinter.ttk as ttk
import AstraBox.WorkSpace as WorkSpace
from AstraBox.Dialogs.Setting import PlotSetting
from AstraBox.Dialogs.Setting import SubPlot

class SubPlotOptionsPanel(ttk.Frame):
    def __init__(self, master, sub_plot: SubPlot, terms: list, on_update_options= None) -> None:
        super().__init__(master)
        self.sub_plot = sub_plot
        self.terms = terms
        self.checked = sub_plot.data
        self.on_update_options = on_update_options
        self.vars = {}
        print(self.checked)
        lbl= tk.Label(self, text ='Title:')
        lbl.grid(row=0, column=0, sticky=tk.W)
        self.sub_plot_title = tk.Label(self, text =sub_plot.title )
        self.sub_plot_title.grid(row= 0, column=1, sticky=tk.W)
        lbl= tk.Label(self, text ='Y label:')
        lbl.grid(row=1, column=0, sticky=tk.W)
        
        self.y_lable_var = tk.StringVar(self, value=sub_plot.y_label)
        self.y_lable_var.trace_add('write', self.update_var)
 
        self.entry = tk.Entry(self, width= 20, textvariable= self.y_lable_var)
        self.entry.grid(row=1, column=1, columnspan=1)      

        self.check_panel = CheckPanel(self, self.terms, self.sub_plot.data, self.update_checked)
        self.check_panel.grid(row=2, column=0, columnspan=2)     


    def update_checked(self):
        self.sub_plot.data = self.check_panel.checked
        if self.on_update_options:
            self.on_update_options()
        
    def update_var(self, var, indx, mode):
        self.sub_plot.y_label = self.y_lable_var.get()
        if self.on_update_options:
            self.on_update_options()

    

class CheckPanel(ttk.Frame):
    num_cols = 3
    ignore = True
    def __init__(self, master, terms: list, checked: list, on_update_checked= None) -> None:
        super().__init__(master)
        self.terms = terms
        self.checked = checked
        self.on_update_checked = on_update_checked
        self.vars = {}
        print(checked)
        for index, term in enumerate(self.terms):
            col = index % self.num_cols
            row = index // self.num_cols
            #print(f'create var: {term}')
            var = tk.IntVar(name= term, value=1 if term in checked else 0)
            checkbutton = tk.Checkbutton(self, text=term, variable=var, command= self.check_clicked )
            self.vars[term] = var
            checkbutton.grid(row= row, column=col, sticky=tk.W)

        self.ignore = False

    def check_clicked(self):
        print(f'check_clicked ')
        checked = []
        for term, v,  in self.vars.items():
            if v.get() > 0:
                print(f'add {term}')
                checked.append(term)
        self.checked = checked
        print(self.checked)
        if self.on_update_checked:
            self.on_update_checked()

    def set_checked(self, checked: list):
        self.ignore = True
        for key, var in self.vars.items():
            var.set(0)
        for term in checked:
            v = self.vars.get(term)
            if v:
                v.set(1)
        self.checked = checked    
        self.ignore = False

    def destroy(self):
        print("CheckPanel destroy")
        super().destroy() 


    def update_var(self, var, indx, mode):
        if self.ignore: return
        (v, tid) = self.vars[var]
        if v.get() > 0:
            print(f'add {var}')
            self.checked.append(var)
        else:
            print(f'remove {var}')
            self.checked.remove(var)
        print(self.checked)
        if self.on_update_checked:
            self.on_update_checked()



class PlotSettingDialog():
    def __init__(self, master, plot_setting: PlotSetting, on_update_setting= None) -> None:
        self.master = master
        self.on_update_setting = on_update_setting
        self.plot_setting = plot_setting

    def show(self):
        win = tk.Toplevel(self.master)
        win.title("Settings")
        win.geometry("220x400")

        tk.Label(win, text =f"Shape {self.plot_setting.shape}" ).pack(padx=5, pady=5, fill=tk.X)

        self.show_grid_var = tk.IntVar(name= 'show grid', value=1 if self.plot_setting.show_grid else 0)
        chkbtn = tk.Checkbutton(win, text='show grid', variable=self.show_grid_var, command= self.show_grid_checked )
        chkbtn.pack(padx=5, pady=5, fill=tk.X)

        if len(self.plot_setting.x_axis_list)>0:
            self.x_axis_var = tk.StringVar(win, value=self.plot_setting.x_axis) 
            combo = ttk.Combobox(win,  textvariable= self.x_axis_var, values=self.plot_setting.x_axis_list)
            combo.pack(padx=5, pady=5, fill=tk.X)
            combo.bind("<<ComboboxSelected>>", self.x_axis_changed)


        self.notebook = ttk.Notebook(win)
        self.notebook.pack(padx=5, pady=5, fill=tk.X)

        for plot in self.plot_setting.sub_plots:
            frame = SubPlotOptionsPanel(self.notebook, plot, self.plot_setting.data_terms, self.update_options)
            self.notebook.add(frame, text=plot.name, underline=0, sticky=tk.NE + tk.SW)

        win.transient(self.master)
        #win.protocol("WM_DELETE_WINDOW", self.on_closing)
        #self.win = win        
        win.grab_set()
        win.focus_set()
        win.wait_window()

    def update_options(self):
        if self.on_update_setting:
            self.on_update_setting()  

    def x_axis_changed(self, event):
        self.plot_setting.x_axis= self.x_axis_var.get()
        if self.on_update_setting:
            self.on_update_setting()        

    def show_grid_checked(self):
        self.plot_setting.show_grid = True if self.show_grid_var.get() == 1 else False
        if self.on_update_setting:
            self.on_update_setting()


    def on_closing(self):
        pass
        #del self.plot_var
        #del self.combo
        #self.check_panel.destroy()
        self.win.destroy()