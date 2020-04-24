from nmigen import *

from . import Peripheral


__all__ = ["BorkPeripheral"]


class BorkPeripheral(Peripheral, Elaboratable):
    def __init__(self):
        super().__init__()

        bank          = self.csr_bank()
        self._wide    = bank.csr(128,"rw")

    def elaborate(self, platform):
        m = Module()
        m.submodules._bridge = self._bridge
        m.d.sync += self._wide.r_data.eq(self._wide.r_data + 1)
        return m
