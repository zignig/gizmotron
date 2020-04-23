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

from plat import BB

class Thing(PeripheralCollection):
    def __init__(self,pwm=None):
        super().__init__()
        #timer1 = TimerPeripheral(32)
        #self.add(timer1)

        timer2 = TimerPeripheral(32)
        self.add(timer2)

#        borker = BorkPeripheral()
#       self.add(borker)

        #blinky = LedPeripheral(Signal(2))
        #.self.add(blinky)
        
        counter = CounterPeripheral(10)
        self.add(counter)

        spi_interface = SPI()
        self.add(spi_interface)

        if pwm is not None:
            pwm = PWM(pwm)
            self.add(pwm)
        
        #self.build()

if __name__ == "__main__":
    from nmigen.cli import pysim
    platform = BB()
    u = platform.request('uart',0)
    u2 = platform.request('uart',1)
    pwm_pin = platform.request('pwm',0)
    uart_divisor = int(platform.default_clk_frequency // 115200 )
    t = Thing(pwm=pwm_pin)
    with pysim.Simulator(t, vcd_file=open("ptest.vcd", "w")) as sim:
        sim.add_clock(10)
        #sim.add_sync_process(sim_data(test_string, mo.sink, mo.source))
        sim.run_until(100000, run_passive=True)
    platform.build(t)
