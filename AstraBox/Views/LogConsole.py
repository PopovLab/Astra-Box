#from asyncio.windows_events import NULL
import datetime
import queue
import logging
import signal
import time
import threading
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk, VERTICAL, HORIZONTAL, N, S, E, W
import os

#logger = logging.getLogger(__name__)

class QueueHandler(logging.Handler):
    """Class to send logging records to a queue

    It can be used from different threads
    The ConsoleUi class polls this queue to display records in a ScrolledText widget
    """
    # Example from Moshe Kaplan: https://gist.github.com/moshekaplan/c425f861de7bbf28ef06
    # (https://stackoverflow.com/questions/13318742/python-logging-to-tkinter-text-widget) is not thread safe!
    # See https://stackoverflow.com/questions/43909849/tkinter-python-crashes-on-new-thread-trying-to-log-on-main-thread

    def __init__(self, log_queue):
        super().__init__()
        self.log_queue = log_queue

    def emit(self, record):
        #print('emit')
        self.log_queue.put(record)


class LogConsole(ScrolledText):
    def __init__(self, master ) -> None:
        super().__init__(master, state='disabled')

        self.configure(font='TkFixedFont')
        self.tag_config('INFO', foreground='black')
        self.tag_config('DEBUG', foreground='gray')
        self.tag_config('WARNING', foreground='orange')
        self.tag_config('ERROR', foreground='red')
        self.tag_config('CRITICAL', foreground='red', underline=1)

    def clear_text(self):
        print('clear log')
        self.configure(state='normal')
        self.delete("1.0", tk.END)
        self.configure(state='disabled')        

    def load_text(self, filename):
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                self.configure(state='normal')
                self.insert(tk.END, f.read())
                self.configure(state='disabled')              
                self.yview(tk.END)
        else:
            self.clear_text()
        

    def set_logger(self, logger):
        # Clear
        self.clear_text()

        # Create a logging handler using a queue
        self.logger = logger
        self.log_queue = queue.Queue()
        self.queue_handler = QueueHandler(self.log_queue)
        formatter = logging.Formatter('%(asctime)s: %(message)s', datefmt='%H:%M:%S')
        self.queue_handler.setFormatter(formatter)
        logger.addHandler(self.queue_handler)
        
        # Start polling messages from the queue
        self.frame.after(100, self.poll_log_queue)        

    def display(self, record):
        #print('display')
        msg = self.queue_handler.format(record)
        self.configure(state='normal')
        self.insert(tk.END, msg + '\n', record.levelname)
        self.configure(state='disabled')
        # Autoscroll to the bottom
        self.yview(tk.END)
        self.update()        


    def poll_log_queue(self):
        # Check every 100ms if there is a new message in the queue to display
        while True:
            try:
                record = self.log_queue.get(block=False)
            except queue.Empty:
                break
            else:
                self.display(record)
        self.frame.after(100, self.poll_log_queue)
