from .gizmo import Gizmo, IO
from nmigen import *

from periph.base import Peripheral,Register

__working__ == False 

@Register(platform="ice40")
class WarmBoot(Peripheral,Elaboratable):
    def __init__(self):
        super().__init__()
        bank = self.csr_bank()
        self._image = bank.csr(2,'w')
        self._en    = bank.csr(1,'w')

    def elaborate(self,platform):
        m = Module()
        m.submodules._bridge = self.bridge

        return m

class _warmboot(Elaboratable):
    def __init__(self):
        self.image = Signal(2, reset=1)
        self.boot = Signal()
        self.ext_boot = Signal()
        self.ext_image = Signal(2)
        self.select = Signal()

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
            image_internal.eq(Mux(self.select, self.ext_image, self.image)),
            boot_internal.eq(Mux(self.select, self.ext_boot, self.boot)),
        ]
        return m


class WarmBoot(Gizmo):
    def build(self, **kwargs):
        w = _warmboot()
        self.ext = w
        self.add_device(w)
        a = IO(sig_out=w.image, name="image")
        self.add_reg(a)
        s = IO(sig_out=w.boot, name="boot")
        self.add_reg(s)
