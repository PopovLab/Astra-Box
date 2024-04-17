import tkinter as tk
import tkinter.ttk as ttk
import AstraBox.Models.ModelFactory as ModelFactory
import AstraBox.WorkSpace as WorkSpace

class TableView(ttk.Frame):
    def __init__(self, master, model_kind= None, height= 5, command= None) -> None:
        super().__init__(master)  
        self.model_kind = model_kind
        self.schema = WorkSpace.get_shema(model_kind)
        WorkSpace.set_binding(model_kind, self)
        self.reverse_sort = True if self.schema.get('reverse_sort') else False
        self.on_select_item = command
        lab = ttk.Label(self, text=self.schema['title'])
        lab.grid(row=0, column=0, sticky=tk.W)
        self.nodes = {}
        self.tree = ttk.Treeview(self,  selectmode="browse", show="", columns=  ( "#1", "#2"), height= height)

        self.tree.heading('#1', text='File')
        #self.tree.heading('#2', text='Comment')
        self.tree.column('#0', stretch=tk.NO)
        self.tree.column('#1', width=30)
        self.tree.column('#2', width=35)
    
        self.update_tree()

        ysb = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        #xsb = ttk.Scrollbar(frame, orient=tk.HORIZONTAL, command=self.tree.xview)

        self.tree.configure(yscroll=ysb.set)

        self.tree.grid(row=1, column=0,  columnspan=2, sticky=tk.N + tk.S + tk.E + tk.W)
        ysb.grid(row=1, column=2, sticky=tk.N + tk.S)
        #xsb.grid(row=2, column=0, sticky=tk.E + tk.W)
        self.tree.bind("<<TreeviewSelect>>", self.select_node)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(1, weight=1)        


    def refresh(self):
        self.update_tree()

    def selection_clear(self):
        print('explorer selection clear')
        self.tree.selection_set(())

    def update_tree(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        self.nodes = {}

        self.models_dict = WorkSpace.get_models_dict(self.model_kind)
        keys_list = sorted(self.models_dict.keys(), reverse= self.reverse_sort) 

        for key in keys_list:
            item = self.models_dict[key]
            #self.tree.insert('', tk.END, text=item.name,  values=(item.name,), tags=('show'))  
            self.tree.insert('', tk.END, text=item.name,  values=(item.name, item.comment,), tags=('show'))  
            
    def select_node(self, event):
        sel_id = self.tree.selection()
        #print(f"selection = {sel_id}")
        if len(sel_id)>0:
            selected_item = self.tree.item(sel_id)
            tag = selected_item["tags"][0]            
            text = selected_item['text']

            action = {
                'action': tag,
                'model_kind' : self.model_kind,
                'data' : self.models_dict.get(text)
                }

            self.on_select_item(self, action)
