from .gizmo import Gizmo, IO
from nmigen import *

# external reset ( used on DTR pin )
# wait for the pin to go hight
# run counter 
# wait for the pin to go low
# if counter < self.second boot into image 0
# else boot into image 1

class ExternalReset(Elaboratable):
    def __init__(self,select,image,boot,pin,status):
        self.select = select
        self.image = image
        self.boot = boot
        self.pin = pin
        self.second = int(32e6)
        self.status = status 

    def elaborate(self,platform):
        m = Module()
        counter = Signal(32)
        enable = Signal()

        with m.If(enable == 1):
            m.d.sync += counter.eq(counter+1)

        m.d.sync += self.status.eq(self.pin) 

        with m.FSM() as fsm:
            with m.State("IDLE"):
                with m.If(self.pin == 0):
                    # start the counter
                    m.next = "WAIT"
            with m.State("WAIT"):
                # wait for the pin to go low
                m.d.sync += enable.eq(1)
                with m.If(self.pin == 1):
                    m.next = "CHOOSE"
            with m.State("CHOOSE"):
                # switch the warmboot to external
                m.d.sync += enable.eq(0)
                m.d.sync += self.select.eq(0)
                # short blip
                with m.If(counter < self.second):
                    m.next = "IMAGE1"
                with m.Else():
                    m.next = "IMAGE2"
            with m.State("IMAGE1"):
                # select image 0
                m.d.sync += self.image.eq(0)
                m.next = "WARMBOOT"
            with m.State("IMAGE2"):
                # select image 1
                m.d.sync += self.image.eq(1)
                m.next = "WARMBOOT"
            with m.State("WARMBOOT"):
                # warmboot
                m.d.sync += self.boot.eq(1)
        return m
