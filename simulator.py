# first cut of boneless simlator

from boneless.arch.asm import Assembler
from boneless.arch.opcode import * 
from boneless.arch.opcode import Instr 

# hard set gateware headers

headers = """
    ; automatic gizmo headers
    .equ blinky,0
    .equ user_led,1
    .equ tx_status,2
    .equ tx_data,3
    .equ rx_status,4
    .equ rx_data,5
    .equ image,6
    .equ boot,7
"""

class SimInstr(object):
    def __init__(self,instr,sim):
        self.instr = instr
        self.sim = sim

    def call(self):
        if self.sim.has_exti:
            print("Exetended instruction")
            self.sim.has_exti = False
            #TODO fix this
        else:
            self.run()

    def __repr__(self):
        return self.instr.__repr__()
    
    # short name access
    @property
    def rsd(self):
        return self.instr.rsd.value

    @property
    def imm(self):
        return self.instr.imm.value

    @property
    def ra(self):
        return self.instr.ra.value 

    def set_reg(self,reg,val):
        self.sim.set_reg(reg,val)

    def reg(self,reg):
        return self.sim.get_reg(reg)

    # simulator function
    @property
    def pc(self):
        return self.sim.pc

    
class s_MOVI(SimInstr):
    def run(self):
        self.set_reg(self.rsd,self.imm)

class s_ADDI(SimInstr):
    def run(self):
        cur = self.reg(self.ra)
        self.sim.set_reg(self.rsd,self.imm+cur)

class s_J(SimInstr):
    def run(self):
        self.sim.set_pc_off(self.imm)

class s_JAL(SimInstr):
    def run(self):
        self.set_reg(self.rsd,self.pc)
        self.sim.set_pc_off(self.imm)

class s_JR(SimInstr):
    def run(self):
        self.sim.set_pc_abs(self.reg(self.rsd))

class s_STXA(SimInstr):
    def run(self):
        print('-->',self.reg(self.rsd))
        self.sim.ext[self.imm] =  self.reg(self.rsd)

class s_LD(SimInstr):
    def run(self):
        self.set_reg(self.rsd,self.sim.mem[self.reg(self.ra)+self.imm])

class s_LDXA(SimInstr):
    def run(self):
        self.set_reg(self.rsd,self.sim.ext[self.imm])


class s_CMPI(SimInstr):
    def run(self):
        out = self.reg(self.ra) - self.imm
        if out == 0:
            self.sim.z = 1
        else:
            self.sim.z = 0

class s_JNZ(SimInstr):
    def run(self):
        if self.sim.z == 0:
            self.sim.set_pc_off(self.imm)
            

class s_JZ(SimInstr):
    def run(self):
        if self.sim.z == 1:
            self.sim.set_pc_off(self.imm)

class s_EXTI(SimInstr):
    def run(self):
        print("E",self.instr.imm.value)
        self.sim.has_exti = True

class s_MOVR(SimInstr):
    def run(self):
        val = self.sim.mem[self.sim.pc+self.imm+1]
        print('movr',self.rsd,val)
        self.sim.set_reg(self.rsd,val)

sim_map = {
        'MOVI':s_MOVI,
        'ADDI':s_ADDI,
        'J':s_J,
        'JR':s_JR,
        'JZ':s_JZ,
        'STXA':s_STXA,
        'CMPI':s_CMPI,
        'JNZ':s_JNZ,
        'EXTI':s_EXTI,
        'JAL': s_JAL,
        'MOVR' : s_MOVR,
        'LDXA' : s_LDXA,
        'LD' : s_LD,
        }


class Simulator:
    def __init__(self,size=200,reset=8,window=0,asm_file="asm/sim_test.asm"):
        self.assembler = Assembler()
        self.asm_file = asm_file
        #self.mem = [0  for i in range(size)]
        self.mem = []
        self.size = size
        self.reset = reset
        self.window = window
        self.pc = reset 
        self.ext = [0 for i in range(20)]
        # flags
        self.z = 0
        self.s = 0
        self.c = 0 
        self.v = 0
        self.has_exti = False

        # assemble the code
        txt = open(self.asm_file).read()
        self.assembler.parse(headers)
        self.assembler.parse(txt)
        self.out = self.assembler.assemble()
        for i,j in enumerate(self.out):
            self.mem.append(j)
    
        # current instruction
        self.current = None
        self.debug = True

    def set_pc_off(self,pos):
        print('set pc',self.pc,pos)
        self.pc = self.pc + pos

    def set_pc_abs(self,pos):
        self.pc = pos

    def get_reg(self,pos):
        assert pos >= 0 & pos < 8
        return self.mem[self.window+pos]

    def set_reg(self,pos,value):
        assert pos >= 0 & pos < 8
        self.mem[self.window+pos] = value

    def step(self):
        val = self.mem[self.pc]
        # if it is an int , convert to an instruction
        if isinstance(val,int):
            instr = self.assembler.disassemble([val])[0]
            cls_name = instr.__class__.__name__
            if cls_name in sim_map:
                sim_instr = sim_map[cls_name](instr,self)
                self.mem[self.pc] = sim_instr
            else:
                print(self.pc,'|',self.mem[0:8],":",instr,"-",val,"|")
                print(cls_name," does not exist")
        
        val = self.mem[self.pc]
        self.current = val

        if isinstance(val,SimInstr):
            val.call()
        if self.debug:
            print(self.pc,self.w,self.current,self.fl)
        self.pc += 1

    @property
    def w(self):
        return self.mem[self.window:self.window+8]

    @property
    def fl(self):
        return [self.z,self.c]

    def run(self,count=1000):
        for i in range(count):
            self.step()

if __name__ == "__main__":
    s = Simulator()
    #s.run(40)
