import os
import json
import tkinter as tk
from pathlib import Path
from pydantic import BaseModel, Field

from AstraBox.Task import Task
import zipfile

_location = None

def get_location_path():
    """get workspace location path"""
    return _location

def temp_folder_location():
    loc = get_location_path().joinpath('tmp')
    if not loc.exists():
        print(f"make dir {loc}")
        loc.mkdir()
    return loc

def get_item_location(model_kind, model_name):
    loc = get_location_path()
    return Path(loc).joinpath(model_name)


class FolderItem():
    def __init__(self, folder,  path:Path) -> None:
        self.parent = folder
        self.name= path.name
        self.path= path
        self.comment= ''
        self.model_kind= folder.content_type
        self.on_update= None
        match path.suffix:
            case '.zip':
                with zipfile.ZipFile(path) as zip:
                    self.comment = zip.comment.decode("utf-8")           
            case _:
                self.comment= ''

    def remove(self)->bool:
        return self.parent.remove(self)

    def delete_file(self)  -> bool:
        print(f'try delete file {self.path}')
        deleted = False
        match self.model_kind:
            case 'RaceModel':
                os.remove(self.path)
                deleted = True
            case _:
                self.path.unlink()
                deleted = True
        print(f'delete status {deleted}')
        return deleted

class Folder(BaseModel):
    title: str
    content_type: str
    required: bool = True
    location: str
    sort_direction: str=  'default'
    tag: str = 'top'
    _root: str
    _observers = set()

    
    def attach(self, observer):
        if (observer not in self._observers):
            self._observers.add(observer)

    def detach(self, observer):
        if (observer in self._observers):
            self.observers.remove(observer)
        
    def raise_event(self, event_name):
        print(event_name)
        for event_observer in self._observers:
            event_observer(event_name)

    def exists(self, root_path)->bool:
        self._location = root_path.joinpath(self.location)
        if self._location.exists():
            return True
        else:
            if self.required:
                print(f"make dir {self._location}")
                self._location.mkdir()
                return True
        return False
    
    def populate(self):
        try:
            self._content = {p.name: FolderItem(self, p) for p in self._location.glob('*.*') if p.name !='.gitignore'}
        except Exception as e:
            print(f"{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: \n{e}")
            self._content = {}

    def refresh(self):
        self.populate()
        self.raise_event('itemsRefresh')

    def remove(self, item)->bool:
        print(f'remove {item.name}')
        ans = tk.messagebox.askquestion(title="Warning", message=f'Delete {item.name}?', icon ='warning')
        removed = False
        if ans == 'yes':
            if item.delete_file():
                self._content.pop(item.name, None)
                self.raise_event('itemsRemoved')
                removed= True
        return removed
    


default_catalog = [
    Folder(title= 'Experiments', content_type='ExpModel', location= 'exp'),
    Folder(title= 'Equlibrium', content_type='EquModel', location= 'equ'),
    Folder(title= 'Subroutine', content_type='SbrModel', location= 'sbr'),
    Folder(title= 'Ray Tracing Configurations', content_type='RTModel', location= 'ray_tracing', required= False),
    Folder(title= 'Race history', content_type='RaceModel', location= 'races', sort_direction= 'reverse', tag= 'bottom'),
]

class WorkSpace(BaseModel):
    folders: list[Folder] = []
    _location: str


    def open(self, path):
        self._location = Path(path)
        for folder in default_catalog:
            if folder.exists(self._location):
                folder.populate()
                self.folders.append(folder)

    def print(self):
        for folder in self.folders:
            print('------')
            print(folder)
            for x in folder._content:
                print(x)

    def folder(self, content_type):
        matches = [x for x in self.folders if x.content_type == content_type]
        if len(matches)>0:
            return matches[0]
        else:
            return None
        
    def folder_content(self, content_type):
        matches = [x for x in self.folders if x.content_type == content_type]
        if len(matches)>0:
            return matches[0]._content
        else:
            return None

    def get_folder_content_list(self, content_type):
        content = self.folder_content(content_type)
        if content:
            return list(content.keys())
        else:
            return []

work_space = None
def get_folder_content_list(content_type):
    if work_space:
        return work_space.get_folder_content_list(content_type)

def folder_content(content_type):
    if work_space:
        return work_space.folder(content_type)._content
        
def refresh_folder(content_type):
    if work_space:
        f = work_space.folder(content_type)
        if f:  f.refresh()

def get_path(content_type: str, sub_path: str= None):
    """get path of workspace folder"""
    if work_space:
        loc = _location.joinpath(work_space.folder(content_type).location)
        if sub_path:
            loc = loc.joinpath(sub_path)
        if not loc.exists():
            print(f"make dir {loc}")
            loc.mkdir()
        return loc
    else:
        return _location

def get_last_task():
    last_task = Task()
    p = get_path('RaceModel').joinpath('last_task')
    if p.exists():
        print(p)
        with p.open(mode= "r") as json_file:
            data = json_file.read()
            last_task = Task.load(data)
    print(last_task)
    return last_task

def save_last_task(last_task):
    p = get_path('RaceModel').joinpath('last_task')
    with p.open(mode= "w") as file:
        file.write(last_task.dump())    


def load_last_run():
    last_run = None
    p = get_path('RaceModel', 'last_run')
    if p.exists():
        with p.open(mode= "r") as json_file:
            last_run = json.load(json_file)
    return last_run

def save_last_run(last_run):
    p = get_path('RaceModel', 'last_run')
    with p.open(mode= "w") as json_file:
        json.dump(last_run, json_file, indent=2)

def open(path):
    global _location
    global work_space
    print(f'Open {path}')
    _location = Path(path)
    work_space = WorkSpace()
    work_space.open(path)
    #work_space.print()
    return work_space

