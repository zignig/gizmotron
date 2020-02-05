# loader program for the bootloader 

def b16(i): return '{:016b}'.format(i)
def b8(i): return '{:08b}'.format(i)

cur_check = 0 

def load(fw):
    sendword(len(fw))
    for i,j in enumerate(fw):
        sendword(j)

def sendword(w):
    high = w >> 8
    low = w & 0xFF
    send(high)
    send(low)

def send(c):
    # should send to the serial port
    print(c)

def getword():
    high = get()
    low = get()
    high_b = high << 8
    val = high_b + low
    return val

def get():
    # get a char from the serial port 
    pass

def checksum(cur,word):
    new = ( cur << 1) ^ word
    cur = new
    return new 


