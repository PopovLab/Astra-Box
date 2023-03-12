import tkinter as tk
import tkinter.ttk as ttk
import AstraBox.Models.ModelFactory as ModelFactory
import AstraBox.WorkSpace as WorkSpace

class Explorer(ttk.Frame):
    def __init__(self, master, title = None, new_button = False, data_source = None, height= 5, reverse_sort= False ) -> None:
        super().__init__(master)  
        self.reverse_sort = reverse_sort    
        self.on_select_item = None
        self.new_button = new_button
        self.data_source = WorkSpace.getDataSource(data_source)
        self.data_source.on_refresh = self.update_tree
        lab = ttk.Label(self, text=title)
        lab.grid(row=0, column=0, sticky=tk.W)
        self.nodes = {}
        self.tree = ttk.Treeview(self,  selectmode="browse", show="tree", columns=  ( "#1"), height= height)
        self.tree.column('#0',stretch=tk.NO)
        self.tree.column('#1', width=40)
        
        
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
        if self.new_button:
            self.tree.insert('', tk.END, text='New ',  tags=('action',))          
        if self.data_source:
            self.make_tree_nodes()

    def make_tree_nodes(self):
        self.data_items = self.data_source.get_items()
        keys_list = sorted(self.data_items.keys(), reverse= self.reverse_sort) 
        for key in keys_list:
            item = self.data_items[key]
            status = ''
            self.tree.insert('', tk.END, text=item.title, values=(status,), tags=(key))  

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
                #model = ModelFactory.create_model(self.model_store.name, 'new model')
                self.on_select_item(self, 'new_model')
            elif self.on_select_item:
                self.on_select_item(self, self.data_items[tag])

