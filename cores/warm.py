from .gizmo import Gizmo, IO
from nmigen import *


class _warmboot(Elaboratable):
    def __init__(self):
        self.image = Signal(2, reset=1)
        self.boot = Signal()
        self.ext_boot = Signal()
        # self.ext_image = Signal(2)

    def elaborate(self, platform):
        m = Module()
        image_internal = Signal(2)
        boot_internal = Signal()
        m.submodules.wb = Instance(
            "SB_WARMBOOT",
            i_S1=image_internal[1],
            i_S0=image_internal[0],
            i_BOOT=boot_internal,
        )
        m.d.comb += [
            image_internal.eq(self.image),
            boot_internal.eq(self.boot | self.ext_boot),
        ]
        return m


class WarmBoot(Gizmo):
    def build(self, **kwargs):
        w = _warmboot()
        self.add_device(w)
        a = IO(sig_out=w.image, name="image")
        self.add_reg(a)
        s = IO(sig_out=w.boot, name="boot")
        self.add_reg(s)
