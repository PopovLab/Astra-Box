import gc
import json
import tkinter as tk
import tkinter
import tkinter.ttk as ttk
import AstraBox.WorkSpace as WorkSpace
from AstraBox.Dialogs.Setting import PlotSetting

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

        self.x_axis_var = tk.StringVar(win, value=self.plot_setting.x_axis) 
        combo = ttk.Combobox(win,  textvariable= self.x_axis_var, values=self.plot_setting.x_axis_list)
        combo.pack(padx=5, pady=5, fill=tk.X)
        combo.bind("<<ComboboxSelected>>", self.x_axis_changed)
        
        plot_names = self.plot_setting.get_sub_plots_names()
        self.plot_var = tk.StringVar(win, value=plot_names[0])   
        self.combo = ttk.Combobox(win,  textvariable= self.plot_var, values=plot_names)
        self.combo.pack(padx=5, pady=5, fill=tk.X)
        self.combo.bind("<<ComboboxSelected>>", self.selected)
        plot = self.plot_var.get()
        sub_plot_0 = self.plot_setting.sub_plots[0]
        self.sub_plot_title = tk.Label(win, text =sub_plot_0.title )
        self.sub_plot_title.pack(padx=5, pady=5, fill=tk.X)
        self.check_panel = CheckPanel(win, self.plot_setting.data_terms, sub_plot_0.data, self.update_checked)
        self.check_panel.pack(padx=5, pady=5, fill=tk.X)

        win.transient(self.master)
        #win.protocol("WM_DELETE_WINDOW", self.on_closing)
        #self.win = win        
        win.grab_set()
        win.focus_set()
        win.wait_window()

    def x_axis_changed(self, event):
        self.plot_setting.x_axis= self.x_axis_var.get()
        if self.on_update_setting:
            self.on_update_setting()        

    def show_grid_checked(self):
        self.plot_setting.show_grid = True if self.show_grid_var.get() == 1 else False
        if self.on_update_setting:
            self.on_update_setting()

    def selected(self, event):
        plot_name = self.plot_var.get()
        sub_plot = self.plot_setting.get_sub_plot(plot_name)
        self.sub_plot_title.config(text = sub_plot.title )
        self.check_panel.set_checked(sub_plot.data)    

    def update_checked(self):
        plot_name = self.plot_var.get()
        sub_plot = self.plot_setting.get_sub_plot(plot_name)
        sub_plot.data = self.check_panel.checked
        if self.on_update_setting:
            self.on_update_setting()

    def on_closing(self):
        pass
        #del self.plot_var
        #del self.combo
        #self.check_panel.destroy()
        self.win.destroy()