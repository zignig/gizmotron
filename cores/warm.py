from .gizmo import Gizmo, IO
from nmigen import *


class _warmboot(Elaboratable):
    def __init__(self):
        self.image = Signal(2)
        self.boot = Signal()

    def elaborate(self, platform):
        m = Module()
        m.submodules.wb = Instance("SB_WARMBOOT",
                i_S1 = self.image[0],
                i_S0 = self.image[1],
                i_BOOT = self.boot
        )
        return m


class WarmBoot(Gizmo):
    def build(self, **kwargs):
        w = _warmboot()
        self.add_device(w)
        a = IO(sig_out=w.image, name="image")
        self.add_reg(a)
        s = IO(sig_out=w.boot, name="boot")
        self.add_reg(s)
