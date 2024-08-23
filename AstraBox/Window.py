import tkinter as tk

count = 1
new_window = True

geo_file = "data/geo.ini"

class Window(tk.Tk):
    '''Opens a new Window.
    '''
    def __init__ (self):
        super().__init__()
        self.title('New Window')
        try:
            # get geometry from file 
            ini_file = open(geo_file,'r')
            self.geometry(ini_file.read())
            
            ini_file.close()
        except:
            print ('error reading geo-file')
            
        self.button_dummy = tk.Button(self, text = f'Do the thing {count}', width = 25, command = lambda : print("Button pressed on window!"))
        self.button_close = tk.Button(self, text = 'Close', width = 25, command = self.close_me)
        self.button_destroy = tk.Button(self, text = 'Destory', width = 25, command = self.destroy_me)
        self.configure_grid()


    def configure_grid(self):
        '''Grid'''
        self.button_dummy.grid(row = 1, column = 0)
        self.button_close.grid(row = 2, column = 0)
        self.button_destroy.grid(row = 3, column = 0)

    def save_geo(self):
            # save current geometry to the ini file 
            try:
                with open(geo_file, 'w') as f:
                    f.write(self.geometry())
                    print('save geo')
                    f.close()
            except:
                print('file error')

    def destroy_me(self):
        global new_window
        new_window = False  
        self.destroy()

    def close_me(self):
        global count
        # Destroys the Widget
        self.save_geo()
        count = count +1
        self.destroy()
