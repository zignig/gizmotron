import serial, time

bl = serial.Serial("/dev/ttyUSB0", 115200,timeout=0.5,dsrdtr=False)

def toggle():
    print('toggle 0')
    bl.dtr = 0
    #time.sleep(1)
    print('toggle 1')
    bl.dtr = 1
    #time.sleep(0.1)
    bl.close()

toggle()

