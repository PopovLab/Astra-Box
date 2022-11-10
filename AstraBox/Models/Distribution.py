import math

def read_from_file(file):
    data = { 'X': [] ,'Y': [] }
    
    lines = file.readlines()
    table = []
    for line in lines:
        #print(line)
        table.append(line.split())

    for row in table:
        for index, (p, item) in enumerate(data.items()):
            #print(p, item, index)
            item.append(float(row[index]))

    return data  


def get(file):

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

    print(len(lines_list))
    len(lines_list[0]['X'])
    return lines_list