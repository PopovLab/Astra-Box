import math
import numpy as np

def float_try(str):
    try:
        return float(str)
    except ValueError:
        #print(str)
        return 0.0

def read_XY_series(file):
    """чтение текстового файла, каждая строка которого вектор типа float
    и создает список из пар {X,Y} """
    data = []
    
    lines = file.readlines()
    x_table = []
    y_table = []
    for index, line in enumerate(lines):
        row = [float_try(v) for v in line.decode("utf-8").split()]
        if index%2 :
            y_table.append(np.array(row))
        else:
            x_table.append(np.array(row))

    for x,y in zip(x_table, y_table):
        data.append({'X':x , 'Y':y})
    return  data


def read_original_distribution_file(file):
    """ чтение оригинального формат в котором сохранялись расределения.
        нет слов что бы его описать ))"""
    def read_from_file(file):
        data = { 'X': [] ,'Y': [] }
    
        lines = file.readlines()
        table = []
        for line in lines:
            table.append(line.split())
        for row in table:
            for index, (p, item) in enumerate(data.items()):
                #print(p, item, index)
                item.append(float(row[index]))
        return data 

    data = read_from_file(file)
    x0 = 0
    lines_list = []
    line = { 'X': [] ,'Y': [], 'logY':[] }
    for x, y in  zip(data['X'], data['Y']):
        if x0<x:
            if y>0:
                line['X'].append(x)
                line['Y'].append(y)
                line['logY'].append(math.log(y))                
            x0 = x
        else:
            lines_list.append(line)
            line = { 'X': [x] ,'Y': [y], 'logY':[math.log(y)] }
            x0 = x
    
    lines_list.append(line)
    
    print(len(lines_list))
    len(lines_list[0]['X'])
    return lines_list