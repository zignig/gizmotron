import opcode_v3  as op
# instruction format
OPCODE_BITS = 5
INSTRUCTION_SIZE = 16
REGISTERS = 8


class grain:
    bits = 1 
    def __init__(self,val):
        self.val = val
        if isinstance(val,str):
            print('string')
        if isinstance(val,int):
            assert val < 2**self.bits
        print(type(val),self.val)

class opcode(grain):
    bits = OPCODE_BITS 

class op4(opcode):
    bits = 4 


class op3(opcode):
    bits = 3


class instruction:
    bits = INSTRUCTION_SIZE
    opcodes = []

        
class register(grain):
    bits = 3

class _type(grain):
    bits = 2


class imm3(grain):
    bits = 3


class imm5(grain):
    bits = 5


class imm8(grain):
    bits = 8


class mode(grain):
    bits = 1

class flag(grain):
    bits = 1

class cond(grain):
    bits = 3

class off8(grain):
    bits = 8

class imm13(grain):
    bits = 13


class RRR(instruction):
    def __init__(self, opc,m,rsd,ra,t,rb):
        self.opcode = op4(opc)
        self.mode = mode(m)
        self.Rsd = register(rsd)
        self.Ra = register(ra)
        self.t = _type(t)
        self.Rb = register(rb)
        self.build = [self.opcode, self.Rsd, self.Ra, self.t, self.Rb]


class RR3(instruction):
    def __init__(self, opc, rsd, ra, t, im):
        self.opcode = opcode(opcode)
        self.Rsd = register(rsd)
        self.Ra = register(ra)
        self.t = _type(t)
        self.i3 = imm3(im)
        self.build = [self.opcode, self.Rsd, self.Ra, self.t, self.i3]


class RR5(instruction):
    def __init__(self, opc,m,rsd,ra,im):
        self.opcode = op4(opc)
        self.mode = mode(m)
        self.Rsd = register(rsd)
        self.Ra = register(ra)
        self.i5 = imm5(im)
        self.build = [self.opcode,self.mode, self.Rsd, self.Ra, self.i5]


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




def AND(ra, rb, rd): return RRR(op.OPCODE4_LOGIC,0, ra, rb, 0b00, rd)
def ANDI(ra, rb, rd): return RRR(op.OPCODE4_LOGIC,1, ra, rb, 0b00, rd)
