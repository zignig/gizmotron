# instruction format
from opcode_v3 import *
import opcode_v3

OPCODE_BITS = 5
INSTRUCTION_SIZE = 16
REGISTERS = 8
debug = False
__all__ = ["AND"]

# symbol resolving function
def res(name):
    print("NO RESOLVER FOR ", name)


resolver = res


class grain:
    bits = 1
    shift = 0
    _resolve = False

    def __init__(self, val):
        if isinstance(val, str):
            # symbol resolution
            self.val = val
            self._resolve = True
        if isinstance(val, int):
            assert val < 2 ** self.bits
            self.val = val

    #            self.val = self.val << self.shift

    def __call__(self):
        return self.val << self.shift

    def s(self):
        return str(self.val)


class opcode(grain):
    bits = OPCODE_BITS


class op4(grain):
    bits = 4
    shift = 1


class op3(grain):
    bits = 3
    shift = 2


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


rev = {}
op_ref = {}


def disam(val):
    opc = val >> 11
    print(op_ref, opc)
    if opc in op_ref:
        print(opc, op_ref[opc])


def collect():
    def inner(cls, *args):
        rev[cls.__qualname__] = cls
        # if cls.opcode in op_ref:
        #    op_ref[cls.opcode].append(cls)
        # else:
        #    op_ref[cls.opcode] = [cls]
        return cls

    return inner


class instruction:
    bits = INSTRUCTION_SIZE

    def __init__(self):
        pass

    #    def __repr__(self):
    #        txt = ''
    #        for i in self.build:
    #            txt += i.s()
    #        return txt

    @property
    def type(self):
        return _type(self.t)

    @property
    def val(self):
        r = self.bits
        val = 0
        # print("--- decompose ---")
        for i in self.build[:-1]:
            print(i, r, i.bits, i.val, "|", bin(i.val), "|")
            if i._resolve:
                i.val = resolver(i.val)
                if i.val is None:
                    raise
            r = r - i.bits
            val += i.val << r
            # print('{:016b}'.format(val))
        i = self.build[-1:][0]
        if i._resolve:
            last = resolver(i.val)
            if last is None:
                raise
        else:
            last = i.val
        val += last
        # print('final')
        print("{:016b}".format(val))
        return val


class RRR(instruction):
    def __init__(self, rsd, ra, rb):
        self.Rsd = register(rsd)
        self.Ra = register(ra)
        self.Rb = register(rb)
        self.build = [self.Rsd, self.Ra, self.type, self.Rb]


class RR3(instruction):
    def __init__(self, rsd, ra, im):
        self.Rsd = register(rsd)
        self.Ra = register(ra)
        self.i3 = imm3(im)
        self.build = [self.Rsd, self.Ra, self.t, self.i3]


class RR5(instruction):
    def __init__(self, rsd, ra, im):
        self.Rsd = register(rsd)
        self.Ra = register(ra)
        self.i5 = imm5(im)
        self.build = [self.Rsd, self.Ra, self.i5]


class R8(instruction):
    def __init__(self, rsd, im):
        self.Rsd = register(rsd)
        self.i8 = imm8(im)
        self.build = [self.Rsd, self.i8]


class C(instruction):
    def __init__(self, c, off):
        self.c = cond(c)
        self.off = off8(off)
        self.build = [self.c, self.off]


class E(instruction):
    def __init__(self, im):
        self.i13 = imm13(im)
        self.build = [self.i13]


class X(instruction):
    def __init__(self, im):
        self.i13 = imm13(im)
        self.build = [self.i13]


# logic
class logic(RRR):
    op4 = OPCODE4_LOGIC
    opt = "OPCODE4_LOGIC"
    mode = 0


class logici(RR3):
    op4 = OPCODE4_LOGIC
    opt = "OPCODE4_LOGIC"
    mode = 1


@collect()
class AND(logic):
    t = OPTYPE2_AND


@collect()
class ANDI(logici):
    t = OPTYPE2_AND


@collect()
class OR(logic):
    t = OPTYPE2_OR


@collect()
class ORI(logici):
    t = OPTYPE2_OR


@collect()
class XOR(logic):
    t = OPTYPE2_XOR


@collect()
class XORI(logici):
    t = OPTYPE2_XOR


@collect()
class CMP(logic):
    t = OPTYPE2_CMP


@collect()
class CMPI(logici):
    t = OPTYPE2_CMP


# arith
class arith(RRR):
    op4 = OPCODE4_ARITH
    mode = 0


class arithi(RR3):
    op4 = OPCODE4_ARITH
    mode = 1


@collect()
class ADD(arith):
    t = OPTYPE2_ADD


@collect()
class ADDI(arithi):
    t = OPTYPE2_ADD


@collect()
class ADC(arith):
    t = OPTYPE2_ADC


@collect()
class ADCI(arithi):
    t = OPTYPE2_ADC


@collect()
class SUB(arith):
    t = OPTYPE2_SUB


@collect()
class SUBI(arithi):
    t = OPTYPE2_SUB


@collect()
class SBB(arith):
    t = OPTYPE2_SBB


@collect()
class SBBI(arithi):
    t = OPTYPE2_SBB


# shift
class shift(RRR):
    op4 = OPCODE4_SHIFT
    mode = 0


class shifti(RR3):
    op4 = OPCODE4_SHIFT
    mode = 1


@collect()
class SLL(shift):
    t = OPTYPE2_SLL


@collect()
class SLLI(shifti):
    t = OPTYPE2_SLL


@collect()
class ROT(shift):
    t = OPTYPE2_ROT


@collect()
class ROTI(shifti):
    t = OPTYPE2_ROT


@collect()
class SRL(shift):
    t = OPTYPE2_SRL


@collect()
class SRLI(shifti):
    t = OPTYPE2_SRL


@collect()
class SRA(shift):
    t = OPTYPE2_SRA


@collect()
class SRAI(shifti):
    t = OPTYPE2_SRA


# 3 Unassigned instructions

# windows and jumps
class window(RRR):
    op4 = OPCODE4_WINDOW
    mode = 0
    t = 0


@collect()
class STW(window):
    Ra = 0b000


@collect()
class SWPW(window):
    Ra = 0b001


@collect()
class ADJW(window):
    Ra = 0b010


@collect()
class ADJW(window):
    Ra = 0b011


# mem


@collect()
class LD(RR5):
    op5 = OPCODE5_LD


@collect()
class LDR(RR5):
    op5 = OPCODE5_LDR


@collect()
class ST(RR5):
    op5 = OPCODE5_ST


@collect()
class STR(RR5):
    op5 = OPCODE5_STR


@collect()
class LDX(RR5):
    op5 = OPCODE5_LDX


@collect()
class LDXA(R8):
    op5 = OPCODE5_LDXA


@collect()
class STX(RR5):
    op5 = OPCODE5_STX


@collect()
class STXA(R8):
    op5 = OPCODE5_STXA


# move


class MOVR(R8):
    op5 = OPCODE5_MOVR


class MOVI(R8):
    op5 = OPCODE5_MOVI


# another unassigned

# jumps


# conditional jumps


class jcc0(C):
    op5 = OPCODE5_JCC0


class jcc1(C):
    op5 = OPCODE5_JCC1


@collect()
class JNZ(jcc0):
    cond = 0b000


@collect()
class JZ(jcc1):
    cond = 0b000


@collect()
class JNE(jcc0):
    cond = 0b000


@collect()
class JE(jcc1):
    cond = 0b000


@collect()
class JNS(jcc0):
    cond = 0b001


@collect()
class JS(jcc1):
    cond = 0b001


@collect()
class JNC(jcc0):
    cond = 0b010


@collect()
class JC(jcc1):
    cond = 0b010


@collect()
class JULT(jcc0):
    cond = 0b010


@collect()
class JUGT(jcc1):
    cond = 0b010


@collect()
class JNO(jcc0):
    cond = 0b011


@collect()
class JO(jcc1):
    cond = 0b011


@collect()
class JUGT(jcc0):
    cond = 0b100


@collect()
class JULE(jcc1):
    cond = 0b100


@collect()
class JSGT(jcc0):
    cond = 0b101


@collect()
class JSLT(jcc1):
    cond = 0b101


@collect()
class JSGT(jcc0):
    cond = 0b110


@collect()
class JSLE(jcc1):
    cond = 0b110


@collect()
class JN(jcc0):
    cond = 0b111


@collect()
class J(jcc1):
    cond = 0b111


@collect()
class JAL(R8):
    op5 = OPCODE5_JAL


# extended
@collect()
class EXTI(E):
    op3 = OPCODE3_EXTI


# custom
class CUST(X):
    op3 = OPCODE3_CUST


# pseudo
def MOV(rd, rs):
    return AND(rd, rs, rs)


def XCHG(rd, rs):
    return [XOR(rd, rd, rs), XOR(rs, rs, rd), XOR(rd, rd, rs)]


def RORI(rd, rs, imm3):
    return ROTI(rd, rs, 16 - imm3)


def info():
    print("instructions")
    l = []
    for i, j in rev.items():
        type_list = j.mro()
        t_v = []
        for k in type_list[:-2]:
            t_v.append(k.__qualname__)
        # t_v.reverse()
        l.append(t_v)
    print(l)
    # reverse them out
    a = {}
    for i in l:
        head = i.pop(0)
        a[head] = i
    for i, j in a.items():
        print(i, j)


def op():
    nl = []
    li = dir(opcode_v3)
    for i in li:
        if i.startswith("O"):
            nl.append(i)
            print(i.split("_"))
    print(nl)
    return nl


info()
op()
# info()
# def ENTR
# def ROLI
# def JALR
# def LEAV
