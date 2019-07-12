#!/usr/bin/python 
from nmigen import *

from boneless_v3.gateware.alsru import ALSRU_4LUT
from boneless_v3.gateware.core_v3 import CoreFSM 
from nmigen import cli


from nmigen.build import ResourceError
from nmigen.build import Resource, Subsignal, Pins

from nmigen_boards.tinyfpga_bx import *

import itertools
# My Current FPGA setup

class BB(TinyFPGABXPlatform):
    resources = TinyFPGABXPlatform.resources + [
        # FTDI link back to pc
        Resource(
            "serial",
            0,
            Subsignal("tx", Pins("19", conn=("gpio", 0), dir="o")),
            Subsignal("rx", Pins("20", conn=("gpio", 0), dir="i")),
        ),
        Resource("user_led", 1, Pins("12", conn=("gpio", 0), dir="o")),
        Resource("user_led", 2, Pins("13", conn=("gpio", 0), dir="o")),
        Resource("user_led", 3, Pins("14", conn=("gpio", 0), dir="o")),
        Resource("user_led", 4, Pins("15", conn=("gpio", 0), dir="o")),
    ]

    def blinky(self):
        leds = []
        for n in itertools.count():
            try:
                l = self.request("user_led", n)
                print(l)
                leds.append(l)
            except ResourceError:
                break

        leds_cat = Cat(led.o for led in leds)
        return leds_cat


class Boneless_v3(Elaboratable):
    def __init__(self, asm_file="asm/base.asm"):
        self.memory = Memory(width=16, depth=2048)  # max of  8*1024 on the 8k

        self.asm_file = asm_file

    def elaborate(self, platform):
        m = Module()
        # Add the platform clock
        clk16 = platform.request("clk16", 0)

        m.domains.sync = ClockDomain()
        m.d.comb += ClockSignal().eq(clk16.i)

        # Create the processor 
        core = CoreFSM(
            alsru_cls=ALSRU_4LUT,
            memory=self.memory,
            reset_pc=8
        )
        m.submodules.core = core
    
        leds = platform.blinky()
        with m.If(core.o_bus_addr == 0):
            with m.If(core.o_ext_we == 1):
                m.d.sync += leds.eq(core.o_ext_data)
            
        return m


if __name__ == "__main__":
    print("Boneless v3")
    platform = BB()
    cpu = Boneless_v3(platform)
    platform.build(cpu, do_program=True)
