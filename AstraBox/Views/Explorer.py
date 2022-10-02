import tkinter as tk
import tkinter.ttk as ttk
import AstraBox.Models.ModelFactory as ModelFactory

class Explorer(ttk.Frame):
    def __init__(self, master, title = None, show_mode = None, model_store = None) -> None:
        super().__init__(master)      
        self.on_select = None
        self.model_store = model_store
        self.model_store.on_update_data = self.update_tree
        lab = ttk.Label(self, text=title)
        lab.grid(row=0, column=0, sticky=tk.W)
        self.nodes = {}
        self.tree = ttk.Treeview(self,  selectmode="browse", show="tree", columns=  ( "#1"), height=5)
        self.tree.column('#0',stretch=tk.NO)
        self.tree.column('#1', width=40, stretch=tk.NO)
        
        
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


    def selection_clear(self):
        print('explorer selection clear')
        self.tree.selection_set(())

    def update_tree(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        self.nodes = {}
        self.tree.insert('', tk.END, text='New ',  tags=('action',))          
        if self.model_store:
            self.make_tree_nodes()

    def make_tree_nodes(self):
        for key in self.model_store.data.keys():
            model = self.model_store.data[key]
            status = 'ok'
            #self.nodes[uuid] = 
            self.tree.insert('', tk.END, text=key, values=(status,), tags=('model'))  

    def select_node(self, event):
        print('Explorer select_node ')
        sel_id = self.tree.selection()
        print(f"selection = {sel_id}")
        if len(sel_id)>0:
            selected_item = self.tree.item(sel_id)
            tag = selected_item["tags"][0]            

            print(selected_item)
            print(tag)
            if tag == 'action':
                print('new')
                model = ModelFactory.create_model(self.model_store.name, 'new model')
                self.on_select(self, model)
            elif self.on_select:
                model = self.model_store.data[selected_item['text']]                           
                self.on_select(self, model)