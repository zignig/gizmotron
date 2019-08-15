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

"""
module pll(
        input  clock_in,
        output clock_out,
        output locked
        );

SB_PLL40_CORE #(
                .FEEDBACK_PATH("SIMPLE"),
                .DIVR(4'b0000),         // DIVR =  0
                .DIVF(7'b0101111),      // DIVF = 47
                .DIVQ(3'b100),          // DIVQ =  4
                .FILTER_RANGE(3'b001)   // FILTER_RANGE = 1
        ) uut (
                .LOCK(locked),
                .RESETB(1'b1),
                .BYPASS(1'b0),
                .REFERENCECLK(clock_in),
                .PLLOUTCORE(clock_out)
                );
i"""	

class WarmBoot(Gizmo):
    def build(self, **kwargs):
        w = _warmboot()
        self.add_device(w)
        a = IO(sig_out=w.image, name="image")
        self.add_reg(a)
        s = IO(sig_out=w.boot, name="boot")
        self.add_reg(s)
