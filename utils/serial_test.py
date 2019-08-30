import serial ,time

bl = serial.Serial('/dev/ttyUSB0',9600)
bl.timeout = 0.01
lines = open('utils/yay.hex').readlines()
v = bl.readall()
print(v)
def load():
    for i in lines:
        val = i.strip().encode('ascii')+str('\r').encode('ascii')
        #print(val)
        bl.write(val)
        v = bl.readall()
        print(v)
load()
