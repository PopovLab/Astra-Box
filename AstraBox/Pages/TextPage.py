import tkinter as tk
import tkinter.ttk as ttk
from tkinter.scrolledtext import ScrolledText
from AstraBox.Views.HeaderPanel import HeaderPanel
import AstraBox.Models.ModelFactory as ModelFactory
import AstraBox.Models.RootModel as RootModel
import AstraBox.WorkSpace as WorkSpace
from AstraBox.Views.TextView import TextView

class TextPage(ttk.Frame):
    def __init__(self, master, folder_item, model) -> None:
        super().__init__(master)        
        self.folder_item= folder_item
        title = f"{model.name}"
        self.header_content = { "title": title, "buttons":[('Save', self.save), ('Delete', self.delete), ('Clone', self.clone)]}
        self.model = model

        self.hp = HeaderPanel(self, self.header_content)
        self.hp.grid(row=0, column=0, columnspan=5, padx=0, sticky=tk.N + tk.S + tk.E + tk.W)

        self.text_view = TextView(self, model)
        self.text_view.grid(row=1, column=0, columnspan=5, padx=10, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

        self.columnconfigure(0, weight=1)             
        self.rowconfigure(1, weight=1)            

    def clone(self):
        new_name = f'{self.model.name}_clone_{RootModel.get_uuid_id()[0:4]}'
        answer = tk.simpledialog.askstring("Clone", "Enter new name", initialvalue= new_name) #,  parent=application_window)
        if answer is not None and answer != '':
            self.model.name = answer
            self.model.path = self.model.path.with_stem(self.model.name)
            self.save()
            WorkSpace.refresh_folder(self.model.model_kind)


    def delete(self):
        #if ModelFactory.delete_model(self.model):
        if self.folder_item.remove():
            self.master.show_empty_view()

    def save(self):
        self.text_view.save()      