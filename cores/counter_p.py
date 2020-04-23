from nmigen import *

from periph.base import Peripheral, Register


__all__ = ["CounterPeripheral"]


@Register(driver="counter")
class CounterPeripheral(Peripheral, Elaboratable):
    def __init__(self, width):
        super().__init__()

        self.width = width

        bank = self.csr_bank()
        self.value = bank.csr(width, "rw")
        self._enable = bank.csr(1, "w")
        self._mark = bank.csr(1, "w")

        self.overflow = self.event(mode="rise")

        self.overflow_count = bank.csr(width, "r")

    def elaborate(self, platform):
        m = Module()

        m.submodules._bridge = self._bridge

        m.d.sync += self.value.r_data.eq(self.value.r_data + 1)
        with m.If(self.value.r_data == 0):
            m.d.sync += [
                self.overflow.stb.eq(1),
                self.overflow_count.r_data.eq(self.overflow_count.r_data + 1),
            ]
        with m.Else():
            m.d.sync += self.overflow.stb.eq(0)
        return m
