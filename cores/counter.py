from .peripheral import Periph, IO, BIT
from nmigen import *


class counter(Elaboratable):
    def __init__(self):
        self.counter = Signal(64)
        self.en = Signal()

    def elaborate(self, platform):
        m = Module()
        with m.If(self.en):
            m.d.sync += self.counter.eq(self.counter + 1)
        return m


class Counter(Periph):
    def build(self):
        c = counter()
        self.add_device(c)
        s = IO(sig_in=c.counter, name=self.name)
        e = IO(sig_in=c.en, name=self.name+"_enable")
        e.add_bit(BIT("enable",0))
        self.add_reg(e)
        self.add_reg(s)
