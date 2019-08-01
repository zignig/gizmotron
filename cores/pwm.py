from .gizmo import Gizmo, IO
from nmigen import *


class _pwm(Elaboratable):
    def __init__(self, pin):
        self.counter = Signal(16)
        self.value = Signal(16)
        self.o = Signal()
        self.active = Signal()
        self.pin = pin

    def elaborate(self, platform):
        m = Module()
        with m.If(self.active):
            m.d.sync += self.counter.eq(self.counter + 1)
            with m.If(self.counter < self.value):
                m.d.sync += self.counter.eq(0)
                m.d.comb += self.o.eq(1)
            with m.Else():
                m.d.comb += self.o.eq(0)
        with m.Else():
            m.d.comb += self.o.eq(0)
        m.d.comb += self.pin.eq(self.o)
        return m


class Pwm(Gizmo):
    def build(self, **kwargs):
        pin = self.platform.request("pwm", 0)
        p = _pwm(pin)
        self.add_device(p)
        a = IO(sig_in=p.active, name="pwm_active")
        self.add_reg(a)
        s = IO(sig_in=p.value, name="pwm_counter")
        self.add_reg(s)
