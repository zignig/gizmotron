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

class BLerror(Exception): pass

class Timeout(BLerror): pass

def toggle(ser,count):
    for i in range(count):
        print('toggle 0')
        time.sleep(0.05)
        ser.dtr = 1
        #time.sleep(0.2)
        print('toggle 1')
        ser.dtr = 0
    ser.dtr = 1

def booload(ser):
    toggle(ser,2)

def warm(ser):
    toggle(ser,4)

def ser_read(ser,length):
    read = b""
    while length > 0:
        new = ser.read(length)
        if len(new) == 0:
            raise Timeout("read timeout")
        read += new
        length -= len(new)
    return read

def read_word(ser):
    data = ser_read(ser,2)
    val = int.from_bytes(data,byteorder="little") 
    print('read',data,"--",val)
    return val 

def write_word(ser,data):
    val = data.to_bytes(2,byteorder="little")
    print('write',val,"--",data)
    ser.write(val)

def load(fwc, port="/dev/ttyUSB0", speed=115200):
    try:
        ser = serial.Serial(port, speed, timeout=1.0,dsrdtr=False,rtscts=False)
    except:
        print("Serial port ", port ," not available")
        return
    
    # get rid of any scrap char
    try:
        ser_read(ser,10)
    except:
        pass
    #warm(ser)
    time.sleep(0.2)
    for i in range(500):
        write_word(ser,i)
        #time.sleep(0.02)
        val = read_word(ser)
        time.sleep(0.01)
        #print(i,val)

    ser.close()

if __name__ == "__main__":
    load([])
