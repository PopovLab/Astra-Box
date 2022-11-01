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
    def __init__(self, master, content, on_select_spectrum) -> None:
        super().__init__(master, relief=tk.FLAT)
        # border=border, borderwidth, class_, cursor, height, name, padding, relief, style, takefocus, width)
        padx = 20
        pady = 5
        v, _ = content[len(content)-1]
        self.value = tk.StringVar(self, v)  # initialize

        for text, command in content:
            btn = ttk.Radiobutton(self, text=text, variable=self.value, value=text, width=25, 
                                command= lambda x = text: on_select_spectrum(x) ,
                                style= 'Toolbutton')
            btn.pack(side=tk.RIGHT, padx=padx, pady=pady)

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

        self.spectrum_type = 'gaussian spectrum'
        radio_content = [('spectrum 2D', None), ('spectrum 1D', None), ('gaussian spectrum', None)]
        self.radio = RadioPanel(self, radio_content, self.on_select_spectrum)
        self.radio.grid(row=5, column=0,columnspan=3, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)

        self.spectrum_view = None
        self.make_spectum_view()
        

    def on_select_spectrum(self, spectrum_type):
        if self.spectrum_type == spectrum_type: return
        if messagebox.askquestion("Spectrum", "Do you want change spectrum?") == 'yes':
            self.spectrum_type = spectrum_type
            self.make_spectum_view()
        else:
            self.radio.value.set(self.spectrum_type)

    def make_spectum_view(self):
        if self.spectrum_view:
            self.spectrum_view.destroy()

        match self.spectrum_type:
            case 'gaussian spectrum':
                self.spectrum_view = SpectrumView.GaussianSpectrumView(self, SpectrumModel(self.model.setting))
                self.spectrum_view.grid(row=6, column=0,columnspan=3, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)            
            case 'spectrum 1D':
                self.spectrum_view = SpectrumView.Spectrum1DView(self, SpectrumModel(self.model.setting))
                self.spectrum_view.grid(row=6, column=0,columnspan=3, padx=5, sticky=tk.N + tk.S + tk.E + tk.W) 
            case 'spectrum 2D':
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