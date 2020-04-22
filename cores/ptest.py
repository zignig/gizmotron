from nmigen import * 
from nmigen_soc.csr import Decoder 
from periph.serial import AsyncSerialPeripheral
from periph.timer import TimerPeripheral 
from periph.bork import BorkPeripheral 
from periph.leds import LedPeripheral 

from peripheral import Peripheral
from counter_p import CounterPeripheral

class Thing:
    def __init__(self):
        p = self.p = Peripheral()
        timer1 = TimerPeripheral(32)
        p.add(timer1)

        t2 = TimerPeripheral(32)
        p.add(t2)

        borker = BorkPeripheral(32)
        p.add(borker)

        blinky = LedPeripheral(Signal(2))
        p.add(blinky)
        
        counter = CounterPeripheral(8)
        p.add(counter)

    def show(self):
        return self.p.show()

t = Thing()
t.show()
