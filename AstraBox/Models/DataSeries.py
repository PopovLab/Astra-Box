import math
import numpy as np

def float_try(str):
    try:
        return float(str)
    except ValueError:
        #print(str)
        return 0.0

def read_from_file(file):
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


def get_maxwell(file):

    data = read_from_file(file)

    return data
