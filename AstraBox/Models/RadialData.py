def float_try(str):
    try:
        return float(str)
    except ValueError:
        return 0.0

def isBlank (myString):
    if myString and myString.strip():
        #myString is not None AND myString is not empty or blank
        return False
    #myString is None OR myString is empty or blank
    return True

def read_radial_data(file):
    header = []
    for i in range(8):
        header.append(file.readline().decode("utf-8"))
    
    #print(header[1])
    #print(header[7])

    radial_data = { h: [] for h in header[7].split() }

    lines = file.readlines()
    table = []
    for line in lines:
        if isBlank(line):
            break
        table.append(line.decode("utf-8").split())
        
    #print(len(table))
  
    for row in table:
        for index, (p, item) in enumerate(radial_data.items()):
            #print(p, item, index)
            item.append(float_try(row[index]))
    i = header[1].find("Time=")
    if i>0:
        time_str = header[1][i+5:].split()[0]
    else:
        time_str = '0.0'
    print(f'time str = {time_str}')
    radial_data['Time'] = float_try(time_str)
    return radial_data
