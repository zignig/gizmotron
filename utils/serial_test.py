import serial 

bl = serial.Serial('/dev/ttyUSB0')
bl.timeout = 0.1

data = open('utils/yay.hex').readlines()
