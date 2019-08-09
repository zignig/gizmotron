
from simi import SimInstr

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

class s_SBB(SimInstr):
   def run(self):
       raise Missing(self)

class s_SBBI(SimInstr):
   def run(self):
       raise Missing(self)

class s_SLL(SimInstr):
   def run(self):
       raise Missing(self)

class s_SLLI(SimInstr):
   def run(self):
       raise Missing(self)

class s_ROT(SimInstr):
   def run(self):
       raise Missing(self)

class s_ROTI(SimInstr):
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
       self
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
       self.set_reg(self.rsd,self.imm)

class s_MOVR(SimInstr):
   def run(self):
       val = self.pc+self.imm+1
       self.set_reg(self.rsd,val)

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
       self.set_reg(self.rsd,self.pc+1)
       self.sim.pc = self.pc+ self.imm

class s_JNZ(SimInstr):
   def run(self):
       raise Missing(self)

class s_JZ(SimInstr):
   def run(self):
       raise Missing(self)

class s_JNS(SimInstr):
   def run(self):
       raise Missing(self)

class s_JS(SimInstr):
   def run(self):
       raise Missing(self)

class s_JNC(SimInstr):
   def run(self):
       raise Missing(self)

class s_JC(SimInstr):
   def run(self):
       raise Missing(self)

class s_JNO(SimInstr):
   def run(self):
       raise Missing(self)

class s_JO(SimInstr):
   def run(self):
       raise Missing(self)

class s_JN(SimInstr):
   def run(self):
       raise Missing(self)

class s_J(SimInstr):
   def run(self):
       self.sim.pc = self.pc + self.imm

class s_JNE(SimInstr):
   def run(self):
       raise Missing(self)

class s_JE(SimInstr):
   def run(self):
       raise Missing(self)

class s_JULT(SimInstr):
   def run(self):
       raise Missing(self)

class s_JUGE(SimInstr):
   def run(self):
       raise Missing(self)

class s_JUGT(SimInstr):
   def run(self):
       raise Missing(self)

class s_JULE(SimInstr):
   def run(self):
       raise Missing(self)

class s_JSGE(SimInstr):
   def run(self):
       raise Missing(self)

class s_JSLT(SimInstr):
   def run(self):
       raise Missing(self)

class s_JSGT(SimInstr):
   def run(self):
       raise Missing(self)

class s_JSLE(SimInstr):
   def run(self):
       raise Missing(self)

class s_EXTI(SimInstr):
   def run(self):
       raise Missing(self)


sim_dict = {
	"AND": s_AND,
	"ANDI": s_ANDI,
	"OR": s_OR,
	"ORI": s_ORI,
	"XOR": s_XOR,
	"XORI": s_XORI,
	"CMP": s_CMP,
	"CMPI": s_CMPI,
	"ADD": s_ADD,
	"ADDI": s_ADDI,
	"ADC": s_ADC,
	"ADCI": s_ADCI,
	"SUB": s_SUB,
	"SUBI": s_SUBI,
	"SBB": s_SBB,
	"SBBI": s_SBBI,
	"SLL": s_SLL,
	"SLLI": s_SLLI,
	"ROT": s_ROT,
	"ROTI": s_ROTI,
	"SRL": s_SRL,
	"SRLI": s_SRLI,
	"SRA": s_SRA,
	"SRAI": s_SRAI,
	"LD": s_LD,
	"LDR": s_LDR,
	"ST": s_ST,
	"STR": s_STR,
	"LDX": s_LDX,
	"LDXA": s_LDXA,
	"STX": s_STX,
	"STXA": s_STXA,
	"MOVI": s_MOVI,
	"MOVR": s_MOVR,
	"STW": s_STW,
	"XCHW": s_XCHW,
	"ADJW": s_ADJW,
	"LDW": s_LDW,
	"JR": s_JR,
	"JRAL": s_JRAL,
	"JVT": s_JVT,
	"JST": s_JST,
	"JAL": s_JAL,
	"JNZ": s_JNZ,
	"JZ": s_JZ,
	"JNS": s_JNS,
	"JS": s_JS,
	"JNC": s_JNC,
	"JC": s_JC,
	"JNO": s_JNO,
	"JO": s_JO,
	"JN": s_JN,
	"J": s_J,
	"JNE": s_JNE,
	"JE": s_JE,
	"JULT": s_JULT,
	"JUGE": s_JUGE,
	"JUGT": s_JUGT,
	"JULE": s_JULE,
	"JSGE": s_JSGE,
	"JSLT": s_JSLT,
	"JSGT": s_JSGT,
	"JSLE": s_JSLE,
	"EXTI": s_EXTI,
}

