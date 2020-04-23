from nmigen import *

from . import Peripheral


__all__ = ["BorkPeripheral"]


class BorkPeripheral(Peripheral, Elaboratable):
    def __init__(self):
        super().__init__()

        bank          = self.csr_bank()
        self._wide    = bank.csr(128,"rw")

        #self._bridge  = self.bridge(data_width=17, granularity=8,alignment=1)
        #self.bus      = self._bridge.bus

    def elaborate(self, platform):
        m = Module()

        m.d.sync += self._wide.eq(self._wide + 1)
        return m
