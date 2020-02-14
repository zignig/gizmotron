
from .simi import SimInstr

class Missing(BaseException):
    pass

class s_AND(SimInstr):
    def run(self):
        raise Missing(self)


class s_ANDI(SimInstr):
    def run(self):
        raise Missing(self)


class s_OR(SimInstr):
    def run(self):
        raise Missing(self)


class s_ORI(SimInstr):
    def run(self):
        raise Missing(self)


class s_XOR(SimInstr):
    def run(self):
        raise Missing(self)


class s_XORI(SimInstr):
    def run(self):
        raise Missing(self)


class s_CMP(SimInstr):
    def run(self):
        raise Missing(self)


class s_CMPI(SimInstr):
    def run(self):
        raise Missing(self)


class s_ADD(SimInstr):
    def run(self):
        raise Missing(self)


class s_ADDI(SimInstr):
    def run(self):
        raise Missing(self)


class s_ADC(SimInstr):
    def run(self):
        raise Missing(self)


class s_ADCI(SimInstr):
    def run(self):
        raise Missing(self)


class s_SUB(SimInstr):
    def run(self):
        raise Missing(self)


class s_SUBI(SimInstr):
    def run(self):
        raise Missing(self)


class s_SBC(SimInstr):
    def run(self):
        raise Missing(self)


class s_SBCI(SimInstr):
    def run(self):
        raise Missing(self)


class s_SLL(SimInstr):
    def run(self):
        raise Missing(self)


class s_SLLI(SimInstr):
    def run(self):
        raise Missing(self)


class s_ROL(SimInstr):
    def run(self):
        raise Missing(self)


class s_ROLI(SimInstr):
    def run(self):
        raise Missing(self)


class s_SRL(SimInstr):
    def run(self):
        raise Missing(self)


class s_SRLI(SimInstr):
    def run(self):
        raise Missing(self)


class s_SRA(SimInstr):
    def run(self):
        raise Missing(self)


class s_SRAI(SimInstr):
    def run(self):
        raise Missing(self)


class s_LD(SimInstr):
    def run(self):
        raise Missing(self)


class s_LDR(SimInstr):
    def run(self):
        raise Missing(self)


class s_ST(SimInstr):
    def run(self):
        raise Missing(self)


class s_STR(SimInstr):
    def run(self):
        raise Missing(self)


class s_LDX(SimInstr):
    def run(self):
        raise Missing(self)


class s_LDXA(SimInstr):
    def run(self):
        raise Missing(self)


class s_STX(SimInstr):
    def run(self):
        raise Missing(self)


class s_STXA(SimInstr):
    def run(self):
        raise Missing(self)


class s_MOVI(SimInstr):
    def run(self):
        raise Missing(self)


class s_MOVR(SimInstr):
    def run(self):
        raise Missing(self)


class s_STW(SimInstr):
    def run(self):
        raise Missing(self)


class s_XCHW(SimInstr):
    def run(self):
        raise Missing(self)


class s_ADJW(SimInstr):
    def run(self):
        raise Missing(self)


class s_LDW(SimInstr):
    def run(self):
        raise Missing(self)


class s_J(SimInstr):
    def run(self):
        raise Missing(self)


class s_JR(SimInstr):
    def run(self):
        raise Missing(self)


class s_JRAL(SimInstr):
    def run(self):
        raise Missing(self)


class s_JVT(SimInstr):
    def run(self):
        raise Missing(self)


class s_JST(SimInstr):
    def run(self):
        raise Missing(self)


class s_JAL(SimInstr):
    def run(self):
        raise Missing(self)


class s_NOP(SimInstr):
    def run(self):
        raise Missing(self)


class s_BZ1(SimInstr):
    def run(self):
        raise Missing(self)


class s_BZ0(SimInstr):
    def run(self):
        raise Missing(self)


class s_BS1(SimInstr):
    def run(self):
        raise Missing(self)


class s_BS0(SimInstr):
    def run(self):
        raise Missing(self)


class s_BC1(SimInstr):
    def run(self):
        raise Missing(self)


class s_BC0(SimInstr):
    def run(self):
        raise Missing(self)


class s_BV1(SimInstr):
    def run(self):
        raise Missing(self)


class s_BV0(SimInstr):
    def run(self):
        raise Missing(self)


class s_BZ(SimInstr):
    def run(self):
        raise Missing(self)


class s_BNZ(SimInstr):
    def run(self):
        raise Missing(self)


class s_BS(SimInstr):
    def run(self):
        raise Missing(self)


class s_BNS(SimInstr):
    def run(self):
        raise Missing(self)


class s_BC(SimInstr):
    def run(self):
        raise Missing(self)


class s_BNC(SimInstr):
    def run(self):
        raise Missing(self)


class s_BV(SimInstr):
    def run(self):
        raise Missing(self)


class s_BNV(SimInstr):
    def run(self):
        raise Missing(self)


class s_BEQ(SimInstr):
    def run(self):
        raise Missing(self)


class s_BGTS(SimInstr):
    def run(self):
        raise Missing(self)


class s_BGTU(SimInstr):
    def run(self):
        raise Missing(self)


class s_BGES(SimInstr):
    def run(self):
        raise Missing(self)


class s_BGEU(SimInstr):
    def run(self):
        raise Missing(self)


class s_BLES(SimInstr):
    def run(self):
        raise Missing(self)


class s_BLEU(SimInstr):
    def run(self):
        raise Missing(self)


class s_BLTS(SimInstr):
    def run(self):
        raise Missing(self)


class s_BLTU(SimInstr):
    def run(self):
        raise Missing(self)


class s_BNE(SimInstr):
    def run(self):
        raise Missing(self)


class s_EXTI(SimInstr):
    def run(self):
        raise Missing(self)




# dict 
d = {
"AND" : s_AND,
"ANDI" : s_ANDI,
"OR" : s_OR,
"ORI" : s_ORI,
"XOR" : s_XOR,
"XORI" : s_XORI,
"CMP" : s_CMP,
"CMPI" : s_CMPI,
"ADD" : s_ADD,
"ADDI" : s_ADDI,
"ADC" : s_ADC,
"ADCI" : s_ADCI,
"SUB" : s_SUB,
"SUBI" : s_SUBI,
"SBC" : s_SBC,
"SBCI" : s_SBCI,
"SLL" : s_SLL,
"SLLI" : s_SLLI,
"ROL" : s_ROL,
"ROLI" : s_ROLI,
"SRL" : s_SRL,
"SRLI" : s_SRLI,
"SRA" : s_SRA,
"SRAI" : s_SRAI,
"LD" : s_LD,
"LDR" : s_LDR,
"ST" : s_ST,
"STR" : s_STR,
"LDX" : s_LDX,
"LDXA" : s_LDXA,
"STX" : s_STX,
"STXA" : s_STXA,
"MOVI" : s_MOVI,
"MOVR" : s_MOVR,
"STW" : s_STW,
"XCHW" : s_XCHW,
"ADJW" : s_ADJW,
"LDW" : s_LDW,
"J" : s_J,
"JR" : s_JR,
"JRAL" : s_JRAL,
"JVT" : s_JVT,
"JST" : s_JST,
"JAL" : s_JAL,
"NOP" : s_NOP,
"BZ1" : s_BZ1,
"BZ0" : s_BZ0,
"BS1" : s_BS1,
"BS0" : s_BS0,
"BC1" : s_BC1,
"BC0" : s_BC0,
"BV1" : s_BV1,
"BV0" : s_BV0,
"BZ" : s_BZ,
"BNZ" : s_BNZ,
"BS" : s_BS,
"BNS" : s_BNS,
"BC" : s_BC,
"BNC" : s_BNC,
"BV" : s_BV,
"BNV" : s_BNV,
"BEQ" : s_BEQ,
"BGTS" : s_BGTS,
"BGTU" : s_BGTU,
"BGES" : s_BGES,
"BGEU" : s_BGEU,
"BLES" : s_BLES,
"BLEU" : s_BLEU,
"BLTS" : s_BLTS,
"BLTU" : s_BLTU,
"BNE" : s_BNE,
"EXTI" : s_EXTI,

}
