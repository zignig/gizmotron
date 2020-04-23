from nmigen import * 
from nmigen_soc.csr import Decoder 
from periph.serial import AsyncSerialPeripheral
from periph.timer import TimerPeripheral 
from periph.bork import BorkPeripheral 
from periph.leds import LedPeripheral 

from periphcollection import PeripheralCollection
from counter_p import CounterPeripheral
from pwm import PWM
from spi import SPI


# Quiet please
Elaboratable._Elaboratable__silence = True

class Thing(PeripheralCollection):
    def __init__(self):
        super().__init__()
        timer1 = TimerPeripheral(32)
        self.add(timer1)

        timer2 = TimerPeripheral(32)
        self.add(timer2)

        borker = BorkPeripheral()
        self.add(borker)

        blinky = LedPeripheral(Signal(2))
        self.add(blinky)
        
        counter = CounterPeripheral(8)
        self.add(counter)

        spi_interface = SPI()
        self.add(spi_interface)

        o = Signal
        pwm = PWM(o)
        self.add(pwm)

t = Thing()
t.show()
