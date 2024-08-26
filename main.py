import tkinter as tk
import AstraBox.App as App
import AstraBox.Window as Window
import AstraBox.History as History

if __name__ == '__main__':
    
    App.work_space = History.get_last()
    
    while App.live:
        print('----')
        App.run()
        #app = App(ws)
        #app.mainloop()
    
    #while Window.new_window:
    #    w = Window.Window()
     #   w.mainloop()
