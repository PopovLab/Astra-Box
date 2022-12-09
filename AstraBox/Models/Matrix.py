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
    for line in lines:
        row = [float_try(v) for v in line.decode("utf-8").split()]
        data.append(row)
    return  np.array(data)  


def get_maxwell(file):

    data = read_from_file(file)

    return data