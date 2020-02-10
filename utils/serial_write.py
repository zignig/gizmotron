import serial, time


def writer(lines, port, speed=9600):
    bl = serial.Serial(port, speed)
    bl.timeout = 0.01
    for i in lines:
        val = i.strip().encode("ascii") + str("\r").encode("ascii")
        # print(val)
        bl.write(val)
        v = bl.readall()
        print(v)
