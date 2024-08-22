import tkinter as tk

count = 1
re_create_flag = True
def re_create():
    global re_create_flag
    global count
    count = count + 1
    re_create_flag = True

def finish():
    global re_create_flag
    re_create_flag = False


class Window(tk.Tk):
    '''Opens a new Window.
    '''
    def __init__ (self):
        super().__init__()
        self.title('New Window')
        self.button_dummy = tk.Button(self, text = f'Do the thing {count}', width = 25, command = lambda : print("Button pressed on window!"))
        self.button_close = tk.Button(self, text = 'Close', width = 25, command = self.close_me)
        self.button_destroy = tk.Button(self, text = 'Destory', width = 25, command = self.destroy_me)
        self.configure_grid()


    def configure_grid(self):
        '''Grid'''
        self.button_dummy.grid(row = 1, column = 0)
        self.button_close.grid(row = 2, column = 0)
        self.button_destroy.grid(row = 3, column = 0)


    def destroy_me(self):
        finish()
        self.destroy()

    def close_me(self):
        # Destroys the Widget
        re_create()
        self.destroy()
