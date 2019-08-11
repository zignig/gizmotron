import itertools
from nmigen import *

from processor import Boneless

# Working gizmos
from cores.gizmo import TestGizmo
from cores.user_leds import UserLeds
from cores.serial import Serial
from cores.counter import Counter
from cores.pwm import Pwm
from cores.warm import WarmBoot

Elaboratable._Elaboratable__silence = True 

# The device construct
def Construct(platform, asm_file="asm/tx.asm"):
    b = Boneless(asm_file=asm_file)

    l = UserLeds("status_leds", platform=platform,source='blinky')
    b.add_gizmo(l)

    l = UserLeds("status", platform=platform,source='user_led')
    b.add_gizmo(l)

    s = Serial(
        "serial_port", platform=platform, number=0, baud=9600
    )
    b.add_gizmo(s)

    wb = WarmBoot("warmboot")
    b.add_gizmo(wb)

    #c = Counter("counter1", platform=platform)
    #b.add_gizmo(c)

    #c2 = Counter("counter2", platform=platform)
    #b.add_gizmo(c2)

    #p = Pwm("pwm",platform=platform,pin=12)
    #b.add_gizmo(p)

    # Assign addresses , get code etch
    # TODO test and fix
    # TODO integrate assembler
    b.prepare()
    return b


# For FPGA
class CPU(Elaboratable):
    def __init__(self, platform, asm_file="asm/blink.asm"):
        self.b = Construct(platform, asm_file=asm_file)
        self.platform = platform

    def elaborate(self, platform):
        clk16 = platform.request("clk16", 0)

        m = Module()
        m.domains.sync = ClockDomain()
        m.d.comb += ClockSignal().eq(clk16.i)

        m.submodules.boneless = self.b
        return m


# For Simulation
class simCPU(Elaboratable):
    def __init__(self, platform, asm_file="asm/blink.asm"):
        self.b = Construct(platform, asm_file=asm_file)
        self.platform = platform
        self.first = Signal(10)
        self.second = Signal(4)
        self.bip = Signal()

    def elaborate(self, platform):
        m = Module()
        m.submodules.boneless = self.b
        with m.If(self.first == self.second):
            m.d.sync += self.bip.eq(1)
        return m


if __name__ == "__main__":
    from plat import BB

    platform = BB()
    import argparse
    from nmigen import cli

    parser = argparse.ArgumentParser()
    cli.main_parser(parser)
    args = parser.parse_args()

    tb = CPU(platform)
    ios = ()
    cli.main_runner(
        parser, args, tb, platform=platform, name="boneless_core", ports=ios
    )
