from nmigen import *

from . import Peripheral


__all__ = ["LedPeripheral"]


class LedPeripheral(Peripheral, Elaboratable):
    """Led peripheral.

    CSR registers
    -------------
    val : read/write
        Set the value of the Leds 
    en : read/write
        Counter enable.
    """
    def __init__(self, leds):
        super().__init__()

        self.leds     = leds

        bank          = self.csr_bank()
        self.led      = bank.csr(16, "rw")
        self._en      = bank.csr(    1, "rw")

        self._bridge  = self.bridge(data_width=16, granularity=8,alignment=1)
        self.bus      = self._bridge.bus

    def elaborate(self, platform):
        m = Module()
        m.submodules.bridge = self._bridge

        with m.If(self._en.r_data):
            m.d.comb += self.leds.eq(self.led.r_data)
        with m.Else():
            m.d.comb += self.leds.eq(0)
        return m
