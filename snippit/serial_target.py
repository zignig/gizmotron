# from http://allican.be/blog/2017/01/15/python-dummy-serial-port.html
import os, pty
from serial import Serial
import threading

def listener(port):
    #continuously listen to commands on the master device
    while 1:
        res  = os.read(port, 1)
        print(res)

def test_serial():
    """Start the testing"""
    master,slave = pty.openpty() #open the pseudoterminal
    s_name = os.ttyname(slave) #translate the slave fd to a filename
    print('connected to ',s_name)

    #create a separate thread that listens on the master device for commands
    thread = threading.Thread(target=listener, args=[master])
    thread.start()

if __name__=='__main__':
    test_serial()
