
__csr_converted__ = False

from nmigen import *
from periph.base import Peripheral

class PWM(Peripheral, Elaboratable):
    def __init__(self,output,width=16,name=None):
        super().__init__()
        bank = self.csr_bank()
        self.width = width
            
        self.enable = bank.csr(1,'rw')
        self.value = bank.csr(width,'rw')
        self.counter = Signal(width+1)

        self._output = Signal()

        self.output = output

        #self._bridge    = self.bridge(data_width=32, granularity=8, alignment=1)
        #self.bus        = self._bridge.bus
        #self.irq        = self._bridge.irq

    def elaborate(self,platform):
        m = Module()

        m.submodules._bridge = self._bridge

        m.d.comb += self.output.eq(self._output)

        with m.If(self.enable.r_data):
            m.d.sync += self.value.r_data.eq(self.value.r_data + 1)
            with m.If(self.counter < self.value):
                m.d.sync += self.counter.eq(0)
                m.d.comb += self._output.eq(1)
            with m.Else():
                m.d.comb += self._output.eq(0)
        with m.Else():
            m.d.comb += self._output.eq(0)

        return m
        
