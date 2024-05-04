import os
import json

def __history_path():
    return os.path.join(os.path.abspath('data'), 'history.json')

def history_exist():
    return os.path.isfile(__history_path())

def get_last():
    a = get_list()
    if len(a)>0:
        return a[-1]
    return None

def get_list():
    if history_exist():
        with open(__history_path(), 'r') as f:
            a = json.loads(f.read())
    else:
        a = []
    return a

def add_new(ws: str):
    a = get_list()
    b = [x for x in a if x!= ws]
    b.append(ws)
    with open(__history_path(), 'w') as f:
        f.write(json.dumps(b))
