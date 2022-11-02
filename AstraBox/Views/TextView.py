import tkinter as tk
import tkinter.ttk as ttk
from tkinter.scrolledtext import ScrolledText
from AstraBox.Views.HeaderPanel import HeaderPanel

class FindToolBar(ttk.Frame):
    def __init__(self, master, text_box) -> None:
        super().__init__(master)
        self.text_box = text_box
        self.query = None
        self.query_var = tk.StringVar(master= self, value='')
        label = tk.Label(master=self, text='Find:')
        label.pack(side = tk.LEFT, ipadx=10)		
        entry = tk.Entry(self, width=55, textvariable= self.query_var)
        entry.pack(side = tk.LEFT, ipadx=10)
        
        btn1 = ttk.Button(self, text= 'Next', command=self.find_next)
        btn1.pack(side = tk.LEFT, ipadx=10)   
    
    def find_first(self):
        #remove tag 'found' from index 1 to END
        print('find first')
        self.text_box.tag_delete("search")
        self.text_box.tag_configure("search", background="yellow")
        start="1.0"
        if len(self.query) > 0:
            self.text_box.mark_set("insert", self.text_box.search(self.query, start))
            self.text_box.see("insert")

        while True:
            pos = self.text_box.search(self.query, start, tk.END) 
            if pos == "": 
                break       
            start = pos + "+%dc" % len(self.query) 
            self.text_box.tag_add("search", pos, "%s + %dc" % (pos,len(self.query)))

    def find_next(self):
        print('find next')
        if self.query != self.query_var.get():
            self.query = self.query_var.get()
            self.find_first()
        # move cursor to end of current match
        while (self.text_box.compare("insert", "<", "end") and
               "search" in self.text_box.tag_names("insert")):
            self.text_box.mark_set("insert", "insert+1c")

        # find next character with the tag
        next_match = self.text_box.tag_nextrange("search", "insert")
        if next_match:
            self.text_box.mark_set("insert", next_match[0])
            self.text_box.see("insert")

        # prevent default behavior, in case this was called
        # via a key binding
        return "break"
     

class TextView(ttk.Frame):
    def __init__(self, master, model) -> None:
        super().__init__(master)        
        #self.title = 'ImpedModelView'
        title = f"Text View {model.name}"
        self.header_content = { "title": title, "buttons":[('Save', self.save), ('Delete', None), ('Clone', None)]}
        self.model = model
        self.hp = HeaderPanel(self, self.header_content)
        self.hp.grid(row=0, column=0, columnspan=5, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)
        self.text_box = ScrolledText(self, bg = "light cyan", wrap="none")
        self.text_box.grid(row=2, column=0, columnspan=5, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)
        self.text_box.insert(tk.END, model.get_text())
        self.find_bat = FindToolBar(self, self.text_box)
        self.find_bat.grid(row=1, column=0, columnspan=5, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)

        self.columnconfigure(0, weight=1)        
        #self.rowconfigure(0, weight=1)            
        self.rowconfigure(2, weight=1)            
        #self.InitUI(model)

    def save(self):
        input = self.text_box.get("1.0",tk.END)
        self.model.save_text(input)
        print(input)