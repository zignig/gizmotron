import serial ,time

bl = serial.Serial('/dev/ttyUSB0',9600)
bl.timeout = 0.02
lines = open('utils/yay.hex').readlines()
print(lines)
def load():
    for i in lines:
        val = i.strip().encode('ascii')+str('\r').encode('ascii')
        for j in val:
            print(j)
            bl.write(j)
            time.sleep(0.1)
            print(bl.read())
load()
