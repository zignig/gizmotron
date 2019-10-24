from nmigen import *
from nmigen_boards.tinyfpga_bx import *
from nmigen_boards.resources.user import LEDResources
from nmigen.build import Resource, Subsignal, Pins, Attrs

"Tiny BX in a BREAD BOARD , with 4 blinky and an FTDI serial "


class BB(TinyFPGABXPlatform):
    resources = TinyFPGABXPlatform.resources + [
        # FTDI link back to pc
        Resource(
            "serial",
            0,
            Subsignal("tx", Pins("19", conn=("gpio", 0), dir="o")),
            Subsignal("rx", Pins("20", conn=("gpio", 0), dir="i")),
        ),
        *LEDResources('blinky',pins="12 13 14 15",conn=("gpio",0),attrs=Attrs(IO_STANDARD="SB_LVCMOS")),
        Resource("pwm", 0, Pins("5", conn=("gpio", 0), dir="o")),
    ]

    clock = "clk16"

    def freq(self):
        clk = self.lookup(self.clock)
        return clk.clock.frequency
