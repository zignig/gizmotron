# instruction format
from opcode_v3 import * 
OPCODE_BITS = 5
INSTRUCTION_SIZE = 16
REGISTERS = 8
debug = False

# symbol resolving function
def res(name):
    print("NO RESOLVER FOR ",name)

resolver = res

class grain:
    bits = 1 
    _resolve = False
    def __init__(self,val):
        if isinstance(val,str):
            # symbol resolution
            self.val = val
            self._resolve = True
        if isinstance(val,int):
            assert val < 2**self.bits
            self.val = val

class opcode(grain):
    bits = OPCODE_BITS 

class op4(grain):
    bits = 4 

class op3(grain):
    bits = 3

        
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


class instruction:
    bits = INSTRUCTION_SIZE
    opcodes = []
    @property
    def val(self):
        r = self.bits 
        val = 0 
        #print("--- decompose ---")
        for i in self.build[:-1]:
            #print(i,r,i.bits,i.val,"|",bin(i.val),"|")
            if i._resolve:
                i.val = resolver(i.val)
                if i.val is None:
                    raise
            r = r - i.bits
            val += i.val << r
            #print('{:016b}'.format(val))
        i = self.build[-1:][0]
        if i._resolve:
            last = resolver(i.val)
            if last is None:
                raise 
        else:
            last = i.val
        val += last
        #print('final')
        print('{:016b}'.format(val))
        return val

class RRR(instruction):
    def __init__(self, opc,m,rsd,ra,t,rb):
        self.opcode = op4(opc)
        self.mode = mode(m)
        self.Rsd = register(rsd)
        self.Ra = register(ra)
        self.t = _type(t)
        self.Rb = register(rb)
        self.build = [self.opcode,self.mode, self.Rsd, self.Ra, self.t, self.Rb]


class RR3(instruction):
    def __init__(self, opc,m, rsd, ra, t, im):
        self.opcode = op4(opc)
        self.mode = mode(m)
        self.Rsd = register(rsd)
        self.Ra = register(ra)
        self.t = _type(t)
        self.i3 = imm3(im)
        self.build = [self.opcode, self.mode,self.Rsd, self.Ra, self.t, self.i3]


class RR5(instruction):
    def __init__(self, opc,rsd,ra,im):
        self.opcode = opcode(opc)
        self.Rsd = register(rsd)
        self.Ra = register(ra)
        self.i5 = imm5(im)
        self.build = [self.opcode,self.Rsd, self.Ra, self.i5]


class R8(instruction):
    def __init__(self, opc,rsd,im):
        self.opcode = opcode
        self.Rsd = register(rsd)
        self.i8 = imm8(im)
        self.build = [self.opcode, self.Rsd, self.i8]


class C(instruction):
    def __init__(self,opc,c,off):
        self.opcode = opcode(opc)
        self.c = cond(c)
        self.off = off8(off)
        self.build = [self.opcode, self.c, self.off]


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



# logic
def AND(ra, rb, rd): return RRR(OPCODE4_LOGIC,0, ra, rb, OPTYPE2_AND, rd)
def ANDI(ra, rb, im): return RR3(OPCODE4_LOGIC,1, ra, rb, OPTYPE2_AND, im)
def OR(ra, rb, rd): return RRR(OPCODE4_LOGIC,0, ra, rb, OPTYPE2_OR, rd)
def ORI(ra, rb, im): return RR3(OPCODE4_LOGIC,1, ra, rb, OPTYPE2_OR, im)
def XOR(ra, rb, rd): return RRR(OPCODE4_LOGIC,0, ra, rb, 0b10, rd)
def XORI(ra, rb, im): return RR3(OPCODE4_LOGIC,1, ra, rb, 0b10, im)
def CMP(ra, rb, rd): return RRR(OPCODE4_LOGIC,0, ra, rb, 0b11, rd)
def CMPI(ra, rb, im): return RR3(OPCODE4_LOGIC,1, ra, rb, 0b11, im)

# arith
def ADD(ra, rb, rd): return RRR(OPCODE4_ARITH,0, ra, rb, 0b00, rd)
def ADDI(ra, rb, im): return RR3(OPCODE4_ARITH,1, ra, rb, 0b00, im)
def ADC(ra, rb, rd): return RRR(OPCODE4_ARITH,0, ra, rb, 0b01, rd)
def ADCI(ra, rb, im): return RR3(OPCODE4_ARITH,1, ra, rb, 0b01, im)
def SUB(ra, rb, rd): return RRR(OPCODE4_ARITH,0, ra, rb, 0b10, rd)
def SUBI(ra, rb, im): return RR3(OPCODE4_ARITH,1, ra, rb, 0b10, im)
def SBB(ra, rb, rd): return RRR(OPCODE4_ARITH,0, ra, rb, 0b11, rd)
def SBBI(ra, rb, im): return RR3(OPCODE4_ARITH,1, ra, rb, 0b11, im)

# shift
def SLL(ra, rb, rd): return RRR(OPCODE4_SHIFT,0, ra, rb, 0b00, rd)
def SLLI(ra, rb, im): return RR3(OPCODE4_SHIFT,1, ra, rb, 0b00, im)
def ROT(ra, rb, rd): return RRR(OPCODE4_SHIFT,0, ra, rb, 0b01, rd)
def ROTI(ra, rb, im): return RR3(OPCODE4_SHIFT,1, ra, rb, 0b01, im)
def SRL(ra, rb, rd): return RRR(OPCODE4_SHIFT,0, ra, rb, 0b10, rd)
def SRLI(ra, rb, im): return RR3(OPCODE4_SHIFT,1, ra, rb, 0b10, im)
def SRA(ra, rb, rd): return RRR(OPCODE4_SHIFT,0, ra, rb, 0b11, rd)
def SRAI(ra, rb, im): return RR3(OPCODE4_SHIFT,1, ra, rb, 0b11, im)

# mem
def LD(rsd,ra,im): return RR5(OPCODE5_LD,rsd,ra,im)
def LDR(rsd,ra,im): return RR5(OPCODE5_LDR,rsd,ra,im)
def ST(rsd,ra,im): return RR5(OPCODE5_ST,rsd,ra,im)
def STR(rsd,ra,im): return RR5(OPCODE5_STR,rsd,ra,im)
def LDX(rsd,ra,off5): return RR5(OPCODE5_LDX,rsd,ra,off5)
def LDXA(rd,off8): return R8(OPCODE5_LDXA,rd,off8)
def STX(rd,off5): return RR5(OPCODE5_STX,rd,ra,off5)
def STXA(rs,off8): return R8(OPCODE5_STXA,rs,off8)

# move 
def MOVR(rsd,im): return R8(OPCODE5_MOVR,rsd,im)
def MOVI(rsd,im): return R8(OPCODE5_MOVI,rsd,im)

# 1001 unassigned 

# windows and jumps
#def SWPW(Rsd,ra,imm3): return RR3(OPCODE_WIN,Rsd,ra,imm3)
#def JR()
#def JALR()
#def JV
#def JT

# jumps

def JNZ(off8): return C(OPCODE5_JCC0,0b000,off8)
def JZ(off8): return C(OPCODE5_JCC1,0b000,off8)
def JNE(off8): return C(OPCODE5_JCC0,0b000,off8)
def JE(off8): return C(OPCODE5_JCC1,0b000,off8)

def JNS(off8): return C(OPCODE5_JCC0,0b000,off8)
def JS(off8): return C(OPCODE5_JCC1,0b001,off8)

def JNC(off8): return C(OPCODE5_JCC0,0b010,off8)
def JC(off8): return C(OPCODE5_JCC1,0b010,off8)
def JULT(off8): return C(OPCODE5_JCC0,0b010,off8)
def JUGE(off8): return C(OPCODE5_JCC1,0b010,off8)

def JNO(off8): return C(OPCODE5_JCC0,0b011,off8)
def JO(off8): return C(OPCODE5_JCC1,0b011,off8)

def JUGT(off8): return C(OPCODE5_JCC0,0b100,off8)
def JULE(off8): return C(OPCODE5_JCC1,0b100,off8)
def JSGE(off8): return C(OPCODE5_JCC0,0b101,off8)
def JSLT(off8): return C(OPCODE5_JCC1,0b101,off8)
def JSGT(off8): return C(OPCODE5_JCC0,0b110,off8)
def JSLE(off8): return C(OPCODE5_JCC1,0b110,off8)

def JN(off8): return C(OPCODE5_JCC0,0b111,off8)
def J(off8): return C(OPCODE5_JCC1,0b111,off8)

def JAL(ra,off8): return R8(OPCODE5_JAL,ra,off8)

# extended
def EXTI(imm): return E(OPCODE3_EXTI,imm)

# custom
def CUST(imm): return X(OPCODE3_CUST,imm13) 

# pseudo
def MOV(rd,rs) : return AND(rd,rs,rs)
def XCHG(rd,rs): return [XOR(rd,rd,rs),XOR(rs,rs,rd),XOR(rd,rd,rs)]
def RORI(rd,rs,imm3): return ROTI(rd,rs,16-imm3)
#def ENTR
#def ROLI
#def JALR
#def LEAV

