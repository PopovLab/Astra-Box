import tkinter as tk
import tkinter.ttk as ttk
import AstraBox.Models.ModelFactory as ModelFactory
import AstraBox.WorkSpace as WorkSpace

class TableView(ttk.Frame):
    def __init__(self, master, folder= None, height= 5, command= None) -> None:
        super().__init__(master)  

        folder.attach(self.folder_handler)
        self.folder = folder   
        self.model_kind = folder.content_type        
        
        #self.schema = WorkSpace.get_shema(model_kind)
        #WorkSpace.set_binding(model_kind, self)
        self.reverse_sort = True 
        self.on_select_item = command
        lab = ttk.Label(self, text= self.folder.title)
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

    def folder_handler(self, event):
        print(f'folder {self.model_kind}')
        print(f'event  {event}')
        self.update_tree()

    def refresh(self):
        self.update_tree()

    def selection_clear(self):
        print('explorer selection clear')
        self.tree.selection_set(())

    def update_tree(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        self.nodes = {}
        self.content = self.folder._content
        if self.content is None:
            return
        keys_list = sorted(self.content.keys(), reverse= self.reverse_sort) 

        for key in keys_list:
            vi = self.content[key]
            if vi.on_update is None:
                vi.on_update = self.update_tree
            #self.tree.insert('', tk.END, text=item.name,  values=(item.name,), tags=('show'))  
            self.tree.insert('', tk.END, text=vi.name,  values=(vi.name, vi.comment,), tags=('show'))  
            
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
                'payload' : self.content.get(text)
                }

            self.on_select_item(self, action)
