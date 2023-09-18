import tkinter as tk
import tkinter.ttk as ttk
from tkinter.scrolledtext import ScrolledText
from AstraBox.Views.HeaderPanel import HeaderPanel
import AstraBox.Models.ModelFactory as ModelFactory
import AstraBox.Models.BaseModel as BaseModel
import AstraBox.WorkSpace as WorkSpace
from AstraBox.Views.TextView import TextView
from AstraBox.Views.ScalarVarsView import ScalarVarsView

class ExpPage(ttk.Frame):
    def __init__(self, master, model) -> None:
        super().__init__(master)        
        #self.title = 'ImpedModelView'
        title = f"{model.name}"
        self.header_content = { "title": title, "buttons":[('Save', self.save), ('Delete', self.delete), ('Clone', self.clone)]}
        self.model = model

        self.hp = HeaderPanel(self, self.header_content)
        self.hp.grid(row=0, column=0, columnspan=5, padx=0, sticky=tk.N + tk.S + tk.E + tk.W)

        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=1, column=0, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)

        text_view = TextView(self, model)
        self.notebook.add(text_view, text="text view", underline=0, sticky=tk.NE + tk.SW)

        scalar_view = ScalarVarsView(self, model)
        self.notebook.add(scalar_view, text="scalar view", underline=0, sticky=tk.NE + tk.SW)

        self.columnconfigure(0, weight=1)             
        self.rowconfigure(1, weight=1)            

    def clone(self):
        new_name = f'{self.model.name}_clone_{BaseModel.get_uuid_id()[0:4]}'
        answer = tk.simpledialog.askstring("Clone", "Enter new name", initialvalue= new_name) #,  parent=application_window)
        if answer is not None and answer != '':
            self.model.name = answer
            self.model.path = self.model.path.with_stem(self.model.name)
            self.save()
            WorkSpace.refresh(self.model.model_kind)


    def delete(self):
        if ModelFactory.delete_model(self.model):
            self.master.show_empty_view()

    def save(self):
        input = self.text_box.get("1.0",tk.END)
        self.model.save_text(input)
        #print(input)            