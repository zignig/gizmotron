# return simulator data 

def char(c):
    d = '{:08b}'.format(ord(c))
    data = []
    for i in d:
        data.append(int(i))

    return data

def str(s):
    data = []
    for i in s:
        data.append(char(i))
    return data


