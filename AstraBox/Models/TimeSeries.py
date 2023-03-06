import math
import numpy as np

def float_try(str):
    try:
        return float(str)
    except ValueError:
        #print(str)
        return 0.0
    
def isBlank (myString):
    if myString and myString.strip():
        #myString is not None AND myString is not empty or blank
        return False
    #myString is None OR myString is empty or blank
    return True

def read_data(file):
    header = file.readline().decode("utf-8").split()
    
    print(header)

    series = { h: [] for h in header }

    lines = file.readlines()
    table = []
    for line in lines:
        if isBlank(line):
            break
        table.append(line.decode("utf-8").split())
        
    #print(len(table))
  
    for row in table:
        for index, (p, item) in enumerate(series.items()):
            #print(p, item, index)
            item.append(float_try(row[index]))

    return series