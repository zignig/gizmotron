" The main construct for the gizmotron"

import itertools
from nmigen import *

from processor import Boneless

# Working periphs
from cores.user_leds import UserLeds
from cores.serial import Serial
from cores.counter import Counter
from cores.pwm import Pwm
from cores.warm import WarmBoot
from cores.pll import pll
from cores.csr_test import csrCounter
from cores.multiply import Multiply

from cores.ext_reset import ExternalReset
from cores.fifo_uart import FIFOUart

Elaboratable._Elaboratable__silence = True

# The device construct
def Construct(platform, fw=None, asm_file=None):
    b = Boneless(fw=fw, asm_file=asm_file)

    l = UserLeds("status_leds", platform=platform, source="blinky")
    b.add_periph(l)

    l = UserLeds("status", platform=platform, source="led")
    b.add_periph(l)

    s = Serial("serial_port", platform=platform, number=0, baud=115200)
    b.add_periph(s)
    #fs = FIFOUart("serial_port",platform=platform ,number=0 , baud=115200,depth=64)
    #b.add_periph(fs)

    wb = WarmBoot("warmboot")
    b.wb_access = wb  # for external warm booter
    b.add_periph(wb)

    # c = Counter('counter1')
    # b.add_periph(c)

    # m = Multiply('multiply')
    # b.add_periph(m)
    b.prepare()

    return b


# For FPGA
class CPU(Elaboratable):
    has_pll = False

    def __init__(self, platform, fw=None, asm_file=None):
        self.b = Construct(platform, fw=fw, asm_file=asm_file)
        self.platform = platform

    def elaborate(self, platform):
        clk = platform.request(platform.default_clk, 0)

        m = Module()
        m.domains.sync = ClockDomain()


        # attach the external reset 
        dtr = platform.request('reset_pin')
        wb = self.b.wb_access.ext
        er = ExternalReset(wb.select,wb.ext_image,wb.ext_boot,dtr)
        m.submodules.reseter = er

        if self.has_pll:
            pl = pll()
            m.d.comb += pl.clock.eq(clk.i)
            m.submodules.pll = pl
            m.d.comb += ClockSignal().eq(pl.out)
        else:
            m.d.comb += ClockSignal().eq(clk.i)

        m.submodules.boneless = self.b
        return m


# For Simulation
class simCPU(Elaboratable):
    def __init__(self, platform, fw=None, asm_file="asm/blink.asm"):
        self.fw = fw
        self.b = Construct(platform, fw=fw, asm_file=asm_file)
        self.platform = platform

    def elaborate(self, platform):
        m = Module()
        m.submodules.boneless = self.b
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
