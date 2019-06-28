# instruction format
OPCODE_BITS = 5
INSTRUCTION_SIZE = 16
REGISTERS = 8


class opcode:
    def __init__(self, opc):
        self.opcode = opc


class op4(opcode):
    pass


class op3(opcode):
    pass


class instruction:
    opcodes = []


class register:
    def __init__(self):
        self.val = 5


class _type:
    bits = 2
    pass


class imm3:
    bits = 3
    pass


class imm5:
    bits = 5
    pass


class imm8:
    bits = 8
    pass


class flag:
    bits = 1
    pass


class cond:
    bits = 3
    pass


class off8:
    bits = 8
    pass


class imm13:
    bits = 13
    pass


class RRR(instruction):
    def __init__(self, opc, ra, rb, t, rsd):
        self.opcode = opcode(opc)
        self.Rsd = register(ra)
        self.Ra = register(rb)
        self.t = _type(t)
        self.Rb = register(rsd)
        build = [self.opcode, self.Rsd, self.Ra, self.t, self.Rb]


class RR3(instruction):
    def __init__(self, opc, rsd, ra, t, im):
        self.opcode = opcode(opcode)
        self.Rsd = register(rsd)
        self.Ra = register(ra)
        self.t = _type(t)
        self.i3 = imm3(im)
        self.build = [self.opcode, self.Rsd, self.Ra, self.t, self.i3]


class RR5(instruction):
    def __init__(self, opc,rsd,ra,im):
        self.opcode = opcode(opc)
        self.Rsd = register(rsd)
        self.Ra = register(ra)
        self.i5 = imm5(im)
        self.build = [self.opcode, self.Rsd, self.Ra, self.i5]


class R8(instruction):
    def __init__(self, opc,rsd,im):
        self.opcode = opcode
        self.Rsd = register(rsd)
        self.i8 = imm8(im)
        self.build = [self.opcode, self.Rsd, self.i8]


class C(instruction):
    def __init__(self,opc,f,c,off):
        self.opcode = op4(opc)
        self.f = flag(f)
        self.c = cond(c)
        self.off = off8(off)
        self.build = [self.opcode, self.f, self.c, self.off]


class E(instruction):
    def __init__(self,opc,im):
        self.opcode = op3(opc)
        self.i13 = imm13(im)
        self.build = [self.opcode,self.i13]


class X(instruction):
    def __init__(self,opc,im):
        self.opcode = op3(opc)
        sel.i13 = imm13(im)
        self.build = [self.opcode,self.i13]




def AND(ra, rb, rd):
    return RRR(0b00000, ra, rb, 0b00, rd)
