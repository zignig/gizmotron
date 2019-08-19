import serial 

bl = serial.Serial('/dev/ttyUSB0')
bl.timeout = 0.1

data = open('utils/yay.hex').read()
def load():
    for i in data:
        bl.write(i.encode())
        print(bl.readall())
load()
