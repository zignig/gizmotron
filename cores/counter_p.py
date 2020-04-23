from nmigen import *

from periph.base import Peripheral,Register


__all__ = ["CounterPeripheral"]

@Register(driver="counter")
class CounterPeripheral(Peripheral, Elaboratable):

    def __init__(self, width):
        super().__init__()

        self.width   = width

        bank          = self.csr_bank()
        self.value = bank.csr(width,"rw")
        self._enable   = bank.csr(1,"w")
        self._mark    = bank.csr(1,"w")

        self.overflow = self.event(mode="rise")

        self.overflow_count = bank.csr(width,'r')

#        self._bridge  = self.bridge(data_width=16, granularity=8,alignment=1)
#        self.bus      = self._bridge.bus

    def elaborate(self, platform):
        m = Module()

        with m.If(self._enable.r_data):
               m.d.sync += self.value.eq(self._wide + 1)
        with m.If(self.value == 0):
            m.d.sync += self.overflow.eq(1)
        return m
