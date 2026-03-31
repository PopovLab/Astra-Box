#from asyncio.windows_events import NULL

import pathlib
import queue
import logging
import tkinter as tk
import re
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk, VERTICAL, HORIZONTAL, N, S, E, W
import os




class LogConsole(ScrolledText):
    def __init__(self, master ) -> None:
        super().__init__(master, state='disabled')

        #self.configure(font='TkFixedFont')
        #self.tag_config('INFO', foreground='black')
        #self.tag_config('DEBUG', foreground='gray')
        #self.tag_config('WARNING', foreground='orange')
        #self.tag_config('ERROR', foreground='red')
        #self.tag_config('CRITICAL', foreground='red', underline=1)

        # Определяем соответствие тегов loguru -> настройки tkinter
        tag_styles = {
            'level':    {'foreground': '#00FF00'},  # по умолчанию зелёный
            'green':    {'foreground': '#00FF00'},
            'red':      {'foreground': '#FF0000'},
            'yellow':   {'foreground': '#FFFF00'},
            'blue':     {'foreground': '#0000FF'},
            'cyan':     {'foreground': '#00FFFF'},
            'magenta':  {'foreground': '#FF00FF'},
            'white':    {'foreground': '#FFFFFF'},
            'bold':     {'font': ('Consolas', 10, 'bold')}
        }
        
        # Регистрируем теги в виджете, если их ещё нет
        for tag, style in tag_styles.items():
            if tag not in self.tag_names():
                self.tag_config(tag, **style)

    def clear_text(self):
        print('clear log')
        self.configure(state='normal')
        self.delete("1.0", tk.END)
        self.configure(state='disabled')        

    def load_text(self, file_path: pathlib.Path):
        try:
            log_text = file_path.read_text(encoding='utf-8')
        except:
            log_text = f'There is no file "{file_path.name}" in the archive.'
        finally:
            self.insert_text(log_text)
        
    def insert_text(self, message):
        self.configure(state='normal')
        self.insert(tk.END, message)
        self.configure(state='disabled')
        self.see(tk.END)
        # Autoscroll to the bottom
        #self.yview(tk.END)
        #self.update()             

    def insert_colored_text(self, raw_message):
        """
        Вставляет текст в виджет, преобразуя цветные теги loguru в теги tkinter.
        Поддерживает теги: <level>, <green>, <red>, <yellow>, <blue>, <cyan>, <magenta>, <white>, <bold>.
        """
        self.configure(state='normal')
        print('------------')
        print(raw_message)
        # Парсим строку с тегами <tag>...</tag> и вставляем порциями
        pattern = r'<(/?)([a-zA-Z0-9_]+)>'
        pos = 0
        stack = []  # стек активных тегов
        for match in re.finditer(pattern, raw_message):
            print('----- match --')
            start, end = match.span()
            print(start, end )
            # Вставляем текст до тега с текущими активными тегами
            if start > pos:
                chunk = raw_message[pos:start]
                # Передаём теги кортежем (если есть)
                self.insert(tk.END, chunk, tuple(stack) if stack else ())
                print(chunk, tuple(stack) if stack else ())
            # Обновляем стек тегов
            tag_name = match.group(2)
            if match.group(1) == '/':  # закрывающий тег
                if stack and stack[-1] == tag_name:
                    stack.pop()
            else:  # открывающий тег
                stack.append(tag_name)
            pos = end
        # Остаток после последнего тега
        if pos < len(raw_message):
            self.insert(tk.END, raw_message[pos:], tuple(stack) if stack else ())
        self.configure(state='disabled')
        self.see(tk.END)
        print('++++++++++++++')