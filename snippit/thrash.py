
from serial import Serial

port = '/dev/ttyUSB0'
speed = 19200

s = Serial(port,speed)
counter = 0
while True:
    s.write('a')
    a = s.read()
    print(a)
    counter +=1
    if counter % 1000:
        print('counter ',counter)

