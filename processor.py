from boneless.arch.instr import *
from boneless.gateware.core import CoreFSM 
from boneless.gateware.alsru import ALSRU_4LUT

from boneless.arch.asm import Assembler

from nmigen import *
from nmigen.back import pysim
from nmigen.cli import main

from cores.gizmo import Gizmo, _GizmoCollection



#TODO move most of this into the gizmo collection object

class Boneless(Elaboratable):
    debug = True
    def __init__(self, asm_file="asm/blink.asm"):
        self.memory = Memory(width=16, depth=2*1024)  # max of  8*1024 on the 8k
        self.asm_file = asm_file

        # Gizmos
        self.gc = _GizmoCollection()
        self._prepared = False

    def add_gizmo(self, giz):
        self.gc += giz

    def insert_gizmos(self, m, platform):
        self.gc.attach(self,m,platform)

    def prepare(self):
        # TODO , map registers bits and code fragments from gizmos
        # Prepare all the gizmos and map their addresses
        self.gc.prepare()
        # generate asm header address list
        header = self.gc.asm_header()

        # Code
        asm = Assembler()
        self.asm = asm
        txt = open(self.asm_file).read()
        asm.parse(header)
        asm.parse(txt)
        #code.load_fragment(header)
        code = asm.assemble()
        self.code = code
        # Object list
        if self.debug:
            print("len :",len(code))
            for i,j in enumerate(asm.input):
                print('{:04X}'.format(i),j)
            for i,j in enumerate(asm.disassemble(code)):
                print('{:04X}'.format(i),j)
        self.bin_code = code
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
        # External port is a better interface
        self.o_bus_addr = core.o_bus_addr
        self.o_ext_we = core.o_ext_we
        self.o_ext_re = core.o_ext_re
        self.o_ext_data = core.o_ext_data
        self.i_ext_data = core.i_ext_data

        self.insert_gizmos(m, platform)
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
