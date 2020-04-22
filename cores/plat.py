from nmigen import *
from nmigen_boards.tinyfpga_bx import *
from nmigen_boards.resources.user import LEDResources
from nmigen_boards.resources.interface import UARTResource
from nmigen.build import Resource, Subsignal, Pins, Attrs

"Tiny BX in a BREAD BOARD , with 4 blinky and an FTDI serial "

plat = TinyFPGABXPlatform

class BB(plat):
    resources = plat.resources + [
        # FTDI link back to pc
        UARTResource(
            0, rx="A8", tx="B8", attrs=Attrs(IO_STANDARD="SB_LVCMOS", PULLUP=1)
        ),
        *LEDResources(
            "blinky", pins="J1 H2 H9 D9", attrs=Attrs(IO_STANDARD="SB_LVCMOS")
        ),
        # CTS on the board ued as reset
        #Resource("status", 0, Pins("12", conn=("gpio", 0), dir="o")),
        Resource("reset_pin", 0, Pins("18", conn=("gpio", 0), dir="i")),
        Resource("pwm", 0, Pins("5", conn=("gpio", 0), dir="o")),
    ]

    flashmap = {
        "device": "AT25SF081-SSHD-B",
        "addrmap": {
            "bootloader": (0x00000, 0x2FFFF),
            "userimage": (0x30000, 0x4FFFF),
            "userdata": (0x50000, 0xFBFFF),
            "desc.tgz": (0xFC000, 0xFFFFF),
        },
    }

    def freq(self):
        clk = self.lookup(self.clock)
        return clk.clock.frequency
