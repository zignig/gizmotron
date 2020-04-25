from nmigen import * 
from nmigen_soc.csr import Decoder 

# peripherals 
from periph.serial import AsyncSerialPeripheral
from periph.timer import TimerPeripheral 
from periph.bork import BorkPeripheral 
from periph.leds import LedPeripheral 

from periphcollection import PeripheralCollection

# new periperals
from counter_p import CounterPeripheral
from pwm import PWM
from spi import SPI
from testperiph import Testing

from plat import BB

import logger
import logging 

logger.level = logging.DEBUG

log = logger.custom_logger(__name__)

class Serial(PeripheralCollection):
    def __init__(self,pwm=None,uart=None,uart_divisor=None,**kwargs):
        super().__init__(**kwargs)
            
        if uart is not None:
            serial1 = AsyncSerialPeripheral(divisor=uart_divisor,pins=uart)
            self.add(serial1)
        

if __name__ == "__main__":
    from nmigen.cli import pysim
    platform = BB()
    u = platform.request('uart',0)
    uart_divisor = int(platform.default_clk_frequency // 115200 )

    t = Serial(uart=u,uart_divisor=uart_divisor)

    with pysim.Simulator(t, vcd_file=open("view_ptest.vcd", "w")) as sim:
        sim.add_clock(10)
        #sim.add_sync_process(sim_data(test_string, mo.sink, mo.source))
        sim.run_until(5000, run_passive=True)
    platform.build(t)
