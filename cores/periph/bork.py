from nmigen import *

from . import Peripheral


__all__ = ["BorkPeripheral"]


class BorkPeripheral(Peripheral, Elaboratable):
    def __init__(self, width):
        super().__init__()

        if not isinstance(width, int) or width < 0:
            raise ValueError("Counter width must be a non-negative integer, not {!r}"
                             .format(width))
        if width > 32:
            raise ValueError("Counter width cannot be greater than 32 (was: {})"
                             .format(width))
        self.width   = width

        bank          = self.csr_bank()
        self._wide    = bank.csr(128,"rw")

        self._bridge  = self.bridge(data_width=16, granularity=8,alignment=1)
        self.bus      = self._bridge.bus

    def elaborate(self, platform):
        m = Module()

        m.d.sync += self._wide.eq(self._wide + 1)
        return m
