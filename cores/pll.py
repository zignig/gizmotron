from .gizmo import Gizmo, IO
from nmigen import *


class pll(Elaboratable):
    def __init__(self):
        self.clock = Signal()
        self.reset = Signal()
        self.lock = Signal()
        self.out = Signal()

    def elaborate(self, platform):
        m = Module()
        m.submodules.pl = Instance("SB_PLL40_CORE",
                p_FEEDBACK_PATH = "SIMPLE",
                p_DIVR= Const(0),
                p_DIVF = Const(47),
                p_DIVQ = Const(4),
                i_REFERENCECLK = self.clock,
                o_LOCK = self.lock,
                o_PLLOUTCORE = self.out,
        )
        return m

"""
FEEDBACK: SIMPLE
F_PFD:   16.000 MHz
F_VCO:  768.000 MHz

DIVR:  0 (4'b0000)
DIVF: 47 (7'b0101111)
DIVQ:  4 (3'b100)

FILTER_RANGE: 1 (3'b001)
"""

"""
F_PLLIN:    16.000 MHz (given)
F_PLLOUT:   20.000 MHz (requested)
F_PLLOUT:   20.000 MHz (achieved)

FEEDBACK: SIMPLE
F_PFD:   16.000 MHz
F_VCO:  640.000 MHz

DIVR:  0 (4'b0000)
DIVF: 39 (7'b0100111)
DIVQ:  5 (3'b101)

FILTER_RANGE: 1 (3'b001)
"""

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
"""	

if __name__ == "__main__":
    print("PLL")
    import argparse
    from nmigen import cli

    parser = argparse.ArgumentParser()
    cli.main_parser(parser)
    args = parser.parse_args()

    tb = pll()
    ios = ()
    cli.main_runner(parser, args, tb, name="pll", ports=ios)
