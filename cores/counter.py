from .gizmo import Gizmo, IO, BIT
from nmigen import *


class counter(Elaboratable):
    def __init__(self):
        self.counter = Signal(16)
        self.en = Signal()

    def elaborate(self, platform):
        m = Module()
        with m.If(self.en):
            m.d.sync += self.counter.eq(self.counter + 1)
        return m


class Counter(Gizmo):
    def build(self):
        c = counter()
        self.add_device(c)
        s = IO(sig_in=c.counter, name="counter")
        e = IO(sig_in=c.en, name="enable")
        e.add_bit(BIT("enable",0))
        self.add_reg(e)
        self.add_reg(s)
