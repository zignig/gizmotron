from boneless.arch.instr import *
from boneless.gateware.core import CoreFSM 
from boneless.gateware.alsru import ALSRU_4LUT

from boneless.arch.asm import Assembler

from nmigen import *
from nmigen.back import pysim
from nmigen.cli import main

from cores.peripheral import Periph, PeriphCollection

from nmigen_soc.csr.bus import * 


class Boneless(Elaboratable):
    debug = True
    def __init__(self, asm_file="asm/blink.asm"):
        self.memory = Memory(width=16, depth=2*1024)  # max of  8*1024 on the 8k
        self.asm_file = asm_file

        # Peripherals
        self._prepared = False
        self.periph = PeriphCollection(data_width=16,addr_width=16)

    def add_periph(self, p):
        self.periph += p 

    def insert_periph(self, m):
        self.periph.attach(m)

    def prepare(self):
        # TODO , map registers bits and code fragments from gizmos
        # Prepare all the gizmos and map their addresses
        self.periph.prepare()
        # generate asm header address list
        header = self.periph.asm_header()
        print(header)
        # Code
        asm = Assembler()
        self.asm = asm
        txt = open(self.asm_file).read()
        asm.parse(header)
        asm.parse(txt)
        code = asm.assemble()
        self.code = code
        # Object list
        if self.debug:
            print("len :",len(code))
            for i,j in enumerate(asm.input):
                print('{:04X}'.format(i),j)
            for i,j in enumerate(asm.disassemble(code)):
                print('{:04X}'.format(i),j)
        self.memory.init = code 
        self.devices = []
        self._prepared = True

    def elaborate(self, platform):
        m = Module()

        m.submodules.core = core = CoreFSM(
            alsru_cls = ALSRU_4LUT,
            reset_pc=8,
            memory = self.memory
        )

        # Bind the csr decoder to the external bus
        m.submodules.csr = csr = self.periph.mplex
        m.d.sync += [
                csr.bus.addr.eq(core.o_bus_addr),
                csr.bus.r_stb.eq(core.o_ext_re),
                csr.bus.w_stb.eq(core.o_ext_we),
                csr.bus.w_data.eq(core.o_ext_data),
                core.i_ext_data.eq(csr.bus.r_data)
        ]
        self.insert_periph(m)
        return m


if __name__ == "__main__":
    import argparse
    from nmigen import cli

    parser = argparse.ArgumentParser()
    cli.main_parser(parser)
    args = parser.parse_args()

    tb = Boneless()
    ios = ()

    cli.main_runner(parser, args, tb, name="boneless_core", ports=ios)
