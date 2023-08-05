import tkinter as tk
import tkinter.ttk as ttk
import os
from pathlib import Path

IMAGE_DIR = Path(os.path.abspath('Images'))
 
def create(parent, image_file, action):
    #print(IMAGE_DIR)
    img = tk.PhotoImage(file=IMAGE_DIR/image_file)
    btn = ttk.Button(parent, image=img, command=action)
    btn.image = img
    return btn

