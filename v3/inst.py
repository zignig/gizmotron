# instruction format
OPCODE_BITS = 5 
INSTRUCTION_SIZE = 16
REGISTERS = 8

class opcode:
    def __init__(self,opc)
        self.opcode = opc

class instruction:
    opcodes = []

class register:
    def __init__(self):
        self.val = 5

class _type:
    pass

class imm3:
    pass

class imm5:
    pass

class imm8:
    pass

class flag:
    pass

class cond:
    pass

class off8:
    pass

class imm13:
    pass

class RRR(instruction):
    def __init__(self,opc,ra,rb,t,rsd):
        self.opcode = opcode(opc)
        self.Rsd = register(ra)
        self.Ra = register(rb)
        self.t = _type(t)
        self.Rb = register(rsd)
        build = [self.opcode,self.Rsd,self.Ra,self.t,self.Rb]


class RR3(instruction):
    def __init__(self,opc,rsd,ra,t,im):
        self.opcode = opcode(opcode)
        self.Rsd = register(rsd)
        self.Ra = register(ra)
        self.t = _type(t)
        self.i3 = imm3(im)
        self.build = [self.opcode,self.Rsd,self.Ra,self.t,self.i3]


class RR5(instruction):
    def __init__(self,opcode):
        self.opcode = opcode
        self.Rsd = register()
        self.Ra = register()
        self.i5 = imm5()
        self.build = [self.opcode,self.Rsd,self.Ra,self.imm5]


class R8(instruction):
    def __init__(self,opcode):
        self.opcode = opcode
        self.Rsd = register()
        self.i8 = imm8()
        self.build = [self.opcode,self.Rsd,self.imm8]


class C(instruction):
    def __init__(self):
        self.f = flag()
        self.c = cond()
        self.off = off8()
        self.build = [self.opcode,self.f,self.c,self.off]


class E(instruction):
    def __init__(self):
        pass


class X(instruction):
    def __init__(self):
        pass

def AND(ra,rb,rd): return RRR(0b00000,ra,rb,0b00,rd)
