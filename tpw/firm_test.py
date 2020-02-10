from boneless.gateware import ALSRU_4LUT, CoreFSM
from boneless.arch.opcode import Instr
from boneless.arch.opcode import *
from boneless.arch.asm import Assembler


def firmware():
    return [
        MOVI(R1, 1024),
        MOVI(R2, 0),
        L("wait"),
        SUBI(R1, R1, 1),
        CMPI(R1, 1024),
        BZ("cont"),
        J("wait"),
        L("cont"),
        ADDI(R2, R2, 1),
        STXA(R2, 32),
        J("wait"),
    ]


def fw():
    a = Assembler()
    f = firmware()
    print(f)
    a.parse(f)
    return a.assemble()
