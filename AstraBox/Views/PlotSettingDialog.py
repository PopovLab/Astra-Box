import gc
import json
import tkinter as tk
import tkinter
import tkinter.ttk as ttk
import AstraBox.WorkSpace as WorkSpace

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
            print(f'create var: {term}')
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
        #for key, (var, tid) in self.vars.items():
            #print(f'delete var: {key}')
            #var.trace_remove('write', tid)
            #del var
        #gc.collect()    
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
    def __init__(self, master, terms: list, file_name: str, default_data= None, on_update_setting= None) -> None:
        self.master = master
        self.terms = terms
        self.file_name = file_name
        self.on_update_setting = on_update_setting
        if default_data:
            self.data = default_data
        else:
            self.data = {}
        loc = WorkSpace.get_location_path().joinpath(file_name)
        if loc.exists():
            with open(loc) as json_file:
                self.data = json.load(json_file)


    def save(self):
        loc = WorkSpace.get_location_path().joinpath(self.file_name)
        with open(loc, "w" ) as json_file:
            json.dump(self.data , json_file, indent = 2 )

    def show(self):
        win = tk.Toplevel(self.master)
        win.title("Settings")
        win.geometry("220x400")


        var = tk.IntVar(name= 'show grid', value=1)
        chkbtn = tk.Checkbutton(win, text='show grid', variable=var, command= self.update_checked )
        chkbtn.pack(padx=5, pady=5, fill=tk.X)
        x_axis_list = ['index', 'ameter', 'rho']
        self.x_axis = tk.StringVar(win, value=x_axis_list[0]) 
        combo = ttk.Combobox(win,  textvariable= self.x_axis, values=x_axis_list)
        combo.pack(padx=5, pady=5, fill=tk.X)
        #!self.vars[term] = var
        #checkbutton.grid(row= row, column=col, sticky=tk.W)
        tk.Label(win, text =f"Shape {self.data['shape']}" ).pack(padx=5, pady=5, fill=tk.X)
        
        plot_names = list(self.data['plots'].keys())
        self.plot_var = tk.StringVar(win, value=plot_names[0])   
        self.combo = ttk.Combobox(win,  textvariable= self.plot_var, values=plot_names)
        self.combo.pack(padx=5, pady=5, fill=tk.X)
        self.combo.bind("<<ComboboxSelected>>", self.selected)
        plot = self.plot_var.get()
        self.check_panel = CheckPanel(win, self.terms, self.data['plots'][plot], self.update_checked)
        self.check_panel.pack(padx=5, pady=5, fill=tk.X)
        self.selected(123)
        win.transient(self.master)
        #win.protocol("WM_DELETE_WINDOW", self.on_closing)
        #self.win = win        
        win.grab_set()
        win.focus_set()
        win.wait_window()


    def selected(self, event):
        plot = self.plot_var.get()
        plot_terms = self.data['plots'][plot]
        self.check_panel.set_checked(plot_terms)    

    def update_checked(self):
        plot = self.plot_var.get()
        self.data['plots'][plot] = self.check_panel.checked
        self.save()
        if self.on_update_setting:
            self.on_update_setting()
        #print(self.data['plots'][plot])


    def on_closing(self):
        pass
        #del self.plot_var
        #del self.combo
        #self.check_panel.destroy()
        self.win.destroy()