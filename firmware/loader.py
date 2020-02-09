# loader program for the bootloader 
import serial 
import time 
import struct

def char(c):
    d = '{:08b}'.format(c)
    data = []
    for i in d:
        data.append(int(i))
    data.reverse()
    return data

def str_data(s):
    data = []
    for i in s:
        data.append(char(i))
    return data

def b16(i): return '{:016b}'.format(i)
def b8(i): return '{:08b}'.format(i)

cur_check = 0 

def convert(fw):
    data = []
    print("firmware length ",len(fw))
    w = len(fw)
    low = w & 0xFF
    high = w >> 8
    data.append(low)
    data.append(high)
    for w in fw:
        print(w)
        low = w & 0xFF
        high = w >> 8
        print(high,low)
        data.append(low)
        data.append(high)
    print(data)
    converted_data = str_data(data)
    return converted_data 

def char_convert(fw):
    data = []
    w = len(fw)
    low = w & 0xFF
    high = w >> 8
    data.append(low)
    data.append(high)
    for w in fw:
        low = w & 0xFF
        high = w >> 8
        data.append(low)
        data.append(high)
    return data 

def load(fwc,port="/dev/ttyUSB0",speed=19200):
    s = serial.Serial(port,speed,timeout=0.1)
    for i in fwc:
        c = s.read()
        val = struct.pack('!B',i)
        print(i,val)
        print('sending '+str(val))
        time.sleep(0.1)
        s.write(val) 
    s.close()

    
