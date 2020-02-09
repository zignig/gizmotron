from boneless.arch.instr import *
from boneless.gateware.core import CoreFSM
from boneless.gateware.alsru import ALSRU_4LUT

from boneless.arch.asm import Assembler

from nmigen import *
from nmigen.back import pysim
from nmigen.cli import main

from cores.gizmo import Gizmo, GizmoCollection
import firmware

# from cores.peripheral import Periph, PeriphCollection
# from nmigen_soc.csr.bus import *


class Boneless(Elaboratable):
    debug = True

    def __init__(self, fw=None, asm_file=None):
        self.memsize = 1 * 512  # max 16 * 512 ok ice40 8k
        self.memory = Memory(width=16, depth=self.memsize)
        self.asm_file = asm_file
        self.code = []
        self.fw = fw

        # Peripherals
        self._prepared = False
        # self.periph = PeriphCollection(data_width=16,addr_width=16)
        self.periph = GizmoCollection(self)

    def add_periph(self, p):
        self.periph += p

    def insert_periph(self, m):
        self.periph.attach(m)

    def prepare(self):
        # TODO , map registers bits and code fragments from gizmos
        # Prepare all the gizmos and map their addresses
        self.periph.prepare()
        # generate asm header address list
        # Code
        if self.asm_file is not None:
            header = self.periph.asm_header()
            print(header)
            asm = Assembler()
            self.asm = asm
            txt = open(self.asm_file).read()
            asm.parse(header)
            asm.parse(txt)
            code = asm.assemble()
            self.code = code
            # Object list
            if self.debug:
                print("len :", len(self.code))
                for i, j in enumerate(asm.disassemble(self.code)):
                    print("{:04X}".format(i), j)
        else:
            print("FIRMWARE ", self.fw)
            io_map = self.periph.io_map()
            self.io_map = io_map
            l = firmware.show()
            if self.fw in l:
                f = firmware.available[self.fw](io_map)
            else:
                raise ValueError("Firmware does not exist")
            f.show()
            self.code = f.assemble()
            # print(f.disassemble())

        self.memory.init = self.code
        self.devices = []
        self._prepared = True

    def elaborate(self, platform):
        m = Module()

        m.submodules.core = core = CoreFSM(
            alsru_cls=ALSRU_4LUT,
            # reset_pc=0,
            memory=self.memory,
            reset_w=self.memsize - 8,
        )

        # Bind the csr decoder to the external bus
        # m.submodules.csr = csr = self.periph.mplex
        # m.d.comb += [
        #        csr.bus.addr.eq(core.o_bus_addr),
        #        csr.bus.r_stb.eq(core.o_ext_re),
        #        csr.bus.w_stb.eq(core.o_ext_we),
        #        csr.bus.w_data.eq(core.o_ext_data),
        #        core.i_ext_data.eq(csr.bus.r_data)
        # ]
        self.o_bus_addr = core.o_bus_addr
        self.o_ext_re = core.o_ext_re
        self.o_ext_we = core.o_ext_we
        self.o_ext_data = core.o_ext_data
        self.i_ext_data = core.i_ext_data

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
