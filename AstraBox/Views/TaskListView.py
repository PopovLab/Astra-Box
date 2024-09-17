import tkinter as tk
import tkinter.ttk as ttk
import AstraBox.Models.ModelFactory as ModelFactory
import AstraBox.WorkSpace as WorkSpace

class TaskListView(ttk.Frame):
    def __init__(self, master, model= None, height= 15, command= None) -> None:
        super().__init__(master)  
        self.model = model   
        self.on_select_item = command
        lab = ttk.Label(self, text= "Task list")
        lab.grid(row=0, column=0, sticky=tk.W)
        self.nodes = {}
        #self.tree = ttk.Treeview(self,  selectmode="browse", show="headings", columns=  ( "#1",  "#2"), height= height)
        self.tree = ttk.Treeview(self,  selectmode="browse", show="headings", columns=  ( "#1",  "#2", "#3"), height= height)

        self.tree.heading('#1', text='index')
        self.tree.heading('#2', text='exp')
        self.tree.heading('#3', text='equ')
        self.tree.column('#0', stretch=tk.NO)
        self.tree.column('#1', width=10)
        self.tree.column('#2', width=10)
        self.tree.column('#2', width=10)
                    
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

    def selection_clear(self):
        print('explorer selection clear')
        self.tree.selection_set(())

    def update_tree(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        self.nodes = {}

        task_list = self.model.task_list
        if task_list:
            #keys_list = sorted(self.content.keys(), reverse= self.reverse_sort) 
            for task in task_list.tasks:
                #item = self.content[key]
                self.tree.insert('', tk.END, text=f'{task.index:05}',  values=(f'{task.index:05}',task.exp, task.equ), tags=('show'))  
                #self.tree.insert('', tk.END, text=item.name,  values=(item.name, 't15 pam 25 ph0 1D',), tags=('show'))  
            
    def select_node(self, event):
        sel_id = self.tree.selection()
        print(f"selection = {sel_id}")
        if len(sel_id)>0:
            selected_item = self.tree.item(sel_id)
            tag = selected_item["tags"][0]            
            text = selected_item['text']
            print(tag)
            print(text)
            index = int(text)
            print(index)
            action = {
                'action': tag,
                'payload' : self.model.task_list.tasks[index]
                }
            print(action)
            if self.on_select_item:
                self.on_select_item(action)
