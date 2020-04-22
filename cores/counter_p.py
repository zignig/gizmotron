from nmigen import *

from periph.base import Peripheral


__all__ = ["CounterPeripheral"]


class CounterPeripheral(Peripheral, Elaboratable):
    def __init__(self, width):
        super().__init__()

        self.width   = width

        bank          = self.csr_bank()
        self._wide    = bank.csr(width,"rw")
        self._enble   = bank.csr(1,"w")

        self._bridge  = self.bridge(data_width=16, granularity=8,alignment=1)
        self.bus      = self._bridge.bus

    def elaborate(self, platform):
        m = Module()

        with m.If(self._enable.r_data):
               m.d.sync += self._wide.eq(self._wide + 1)

        return m
