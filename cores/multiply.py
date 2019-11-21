from .peripheral import Periph, IO
from nmigen import *


class _multiply(Elaboratable):
    def __init__(self):
        self.a = Signal(16)
        self.b = Signal(16)
        self.o = Signal(32)

    def elaborate(self, platform):
        m = Module()
        m.d.comb += self.o.eq(self.a*self.b)
        return m


class Multiply(Periph):
    def build(self, **kwargs):
        m = _multiply()
        self.add_device(m)
        a = IO(sig_out=m.a, name="mulopa")
        self.add_reg(a)
        b = IO(sig_out=m.b, name="mulopb")
        self.add_reg(b)
        o = IO(sig_in=m.o, name="mulout")
        self.add_reg(o)
