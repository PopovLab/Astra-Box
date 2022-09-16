import tkinter as tk
import tkinter.ttk as ttk

class Explorer(ttk.Frame):
    def __init__(self, master, title = None, show_mode = None) -> None:
        super().__init__(master)      
        self.on_select = None
        #self.storage = store
        lab = ttk.Label(self, text=title)
        lab.grid(row=0, column=0, sticky=tk.W)
        self.nodes = {}
        self.tree = ttk.Treeview(self,  selectmode="browse", show="tree", columns=  ( "#1"), height=5)
        self.tree.column('#0',stretch=tk.NO)
        self.tree.column('#1', width=40, stretch=tk.NO)
        
        
        #self.update_tree()

        ysb = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        #xsb = ttk.Scrollbar(frame, orient=tk.HORIZONTAL, command=self.tree.xview)

        self.tree.configure(yscroll=ysb.set)

        self.tree.grid(row=1, column=0,  columnspan=2, sticky=tk.N + tk.S + tk.E + tk.W)
        ysb.grid(row=1, column=2, sticky=tk.N + tk.S)
        #xsb.grid(row=2, column=0, sticky=tk.E + tk.W)
        #self.tree.bind("<<TreeviewSelect>>", self.select_node)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(1, weight=1)        
