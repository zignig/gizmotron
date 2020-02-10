# loader program for the bootloader
import serial
import time
import struct

"""
This is the serial interface for the bootloader

~ singlc char echo works
~ word echo works

TODO

- look into handshake and ID in uloader
- running check sum and cross boot

##next to try

write to mem
read back from mem
see firmaware/uloader.py for TODOS


"""


def char(c):
    d = "{:08b}".format(c)
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


def b16(i):
    return "{:016b}".format(i)


def b8(i):
    return "{:08b}".format(i)


cur_check = 0


def convert(fw):
    data = []
    print("firmware length ", len(fw))
    w = len(fw)
    low = w & 0xFF
    high = w >> 8
    data.append(low)
    data.append(high)
    for w in fw:
        print(w)
        low = w & 0xFF
        high = w >> 8
        print(high, low)
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


def load(fwc, port="/dev/ttyUSB0", speed=115200):
    s = serial.Serial(port, speed, timeout=0.018)
    # fwc += fwc
    last = 0
    for i, j in enumerate(fwc):
        val = struct.pack("!B", j)
        # time.sleep(0.1)
        s.write(val)
        c = s.read(1)
        print(i, "\t", struct.unpack("!B", c)[0], "\t", struct.unpack("!B", val)[0])
        if i > 2:
            if c != last:
                print("FAIL")
                break
        last = val
    s.close()
