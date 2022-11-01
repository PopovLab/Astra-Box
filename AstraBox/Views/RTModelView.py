import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox

from AstraBox.Models.SpectrumModel import SpectrumModel
from AstraBox.Views.HeaderPanel import HeaderPanel
import AstraBox.Widgets as Widgets
import AstraBox.Views.SpectrumView as SpectrumView
import AstraBox.Models.ModelFactory as ModelFactory
import AstraBox.WorkSpace as WorkSpace


class RadioPanel(ttk.Frame):
    def __init__(self, master, spectrum_model, on_change_spectrum) -> None:
        super().__init__(master, relief=tk.FLAT)
        self.spectrum_model = spectrum_model
        self.on_change_spectrum = on_change_spectrum
        # border=border, borderwidth, class_, cursor, height, name, padding, relief, style, takefocus, width)
        padx = 20
        pady = 5
        #v, _ = content[len(content)-1]
        self.value = tk.StringVar(self, spectrum_model.spectrum_type)  # initialize

        for text, key in spectrum_model.get_ratio_content():
            btn = ttk.Radiobutton(self, text=text, variable=self.value, value=key, width=25, 
                                command= lambda x = key: self.on_radio_select(x) ,
                                style= 'Toolbutton')
            btn.pack(side=tk.RIGHT, padx=padx, pady=pady)
    
    def on_radio_select(self, value):
        if self.spectrum_model.spectrum_type == value: return
        if messagebox.askquestion("Spectrum", "Do you want change spectrum?") == 'yes':
            self.spectrum_model.spectrum_type = value
            self.on_change_spectrum()
        else:
            self.radio.value.set(self.spectrum_model.spectrum_type)


class RTModelView(ttk.Frame):
    def __init__(self, master, model) -> None:
        super().__init__(master)        
        #self.title = 'ImpedModelView'
        title = f"RT Configuration View {model.name}"
        if model.name == 'new model':
            self.header_content = { "title": title, "buttons":[('Save', self.save_model)]}
        else:    
            self.header_content = { "title": title, "buttons":[('Save', self.save_model), ('Delete', self.delete_model), ('Clone', None)]}
        self.model = model
        self.hp = HeaderPanel(self, self.header_content)
        self.hp.grid(row=0, column=0, columnspan=5, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)
        #self.label = ttk.Label(self,  text='ImpedModelView')
        #self.label.place(relx=0.5, rely=0.46, anchor=tk.CENTER)
        #self.label.grid(row=0, column=0, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)
        self.columnconfigure(0, weight=0)        
        self.columnconfigure(1, weight=1)         
        #self.rowconfigure(0, weight=1)            
        #self.InitUI(model)

        self.label = ttk.Label(self,  text='Name:')
        self.label.grid(row=1, column=0, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W)
        self.var_name = tk.StringVar(master= self, value=self.model.name)
        self.name_entry = ttk.Entry(self, textvariable = self.var_name)
        self.name_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

        self.label = ttk.Label(self,  text='Comment:')
        self.label.grid(row=2, column=0, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)
        self.comment_text = tk.Text(self, height=3,  wrap="none")
        self.comment_text.grid(row=2, column=1, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)
        self.comment_text.insert(tk.END, self.model.setting['Comments']['value'])

        self.notebook = ttk.Notebook(self)
        #self.notebook.pack(side="top", expand=1, fill="both", pady=6, padx=6)
        self.notebook.grid(row=4, column=0,columnspan=3, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)
        
        ROW_MAX = 7 
        for key, value in self.model.setting.items():
            if 'value' in value:
                continue
            if key == 'spectrum':
                continue            
            frame = ttk.Frame(self.notebook)  
            self.notebook.add(frame, text=key, underline=0, sticky=tk.NE + tk.SW)
            for row, (_, item) in enumerate(value.items()):
                wg = Widgets.create_widget(frame, item)
                wg.grid(row=row%ROW_MAX, column=row//ROW_MAX, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)

        self.spectrum_model = SpectrumModel(self.model.setting)
        
        self.radio = RadioPanel(self, self.spectrum_model, self.make_spectum_view)
        self.radio.grid(row=5, column=0,columnspan=3, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)

        self.spectrum_view = None
        self.make_spectum_view()
        
  
    def make_spectum_view(self):
        if self.spectrum_view:
            self.spectrum_view.destroy()
        print(self.spectrum_model.spectrum_type)
        match self.spectrum_model.spectrum_type:
            case 'gaussian':
                self.spectrum_view = SpectrumView.GaussianSpectrumView(self, self.spectrum_model)
                self.spectrum_view.grid(row=6, column=0,columnspan=3, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)            
            case 'spectrum_1D':
                self.spectrum_view = SpectrumView.Spectrum1DView(self, self.spectrum_model)
                self.spectrum_view.grid(row=6, column=0,columnspan=3, padx=5, sticky=tk.N + tk.S + tk.E + tk.W) 
            case 'spectrum_2D':
                pass
        
        

    def save_model(self):
        if self.var_name.get() == 'new model':
            tk.messagebox.showwarning(title=None, message='Please, change model name')
            return        
        self.model.name = self.var_name.get()
        self.model.setting['Comments']['value'] = self.comment_text.get("1.0",tk.END)
        self.model.path = self.model.path.with_stem(self.model.name)
        #if self.model.name in Storage().rt_store.data:
        #    tk.messagebox.showwarning(title=None, message=f'{self.model.name} exist in store! \n Please, change model name')
        #    return
        #Storage().rt_store.save_model(self.model)
        self.model.save_to_json()
        WorkSpace.getDataSource('ray_tracing').refresh() 
    
    def delete_model(self):
        if ModelFactory.delete_model(self.model):
            self.master.show_empty_view()