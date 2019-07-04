from nmigen import *

from boneless_v3.gateware.alsru import ALSRU_4LUT
from boneless_v3.gateware.core_v3 import CoreFSM 
from nmigen import cli
def v3():
    memory = Memory(width=16, depth=256)
    memory.init = [0b10000_111_10101010] # MOVI R7, 0xAA
    dut = CoreFSM(alsru_cls=ALSRU_4LUT, memory=memory)
    ports = (
        dut.o_bus_addr,
        dut.i_ext_data, dut.o_ext_re, dut.o_ext_data, dut.o_ext_we,
    )
v3()
