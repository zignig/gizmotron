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
class SimInstr:
    def __init__(self,instr,sim):
        self.instr = instr
        self.sim = sim

    def run(self):
        pass

class s_MOVI(SimInstr):
    def run(self):
        reg = self.instr.rsd.value
        val = self.instr.imm.value
        self.sim.set_reg(reg,val)

class s_ADDI(SimInstr):
    def run(self):
        reg = self.instr.rsd.value
        val = self.instr.imm.value
        cur = self.sim.get_reg(reg)
        self.sim.set_reg(reg,val+cur)

class s_J(SimInstr):
    def run(self):
        self.sim.set_pc_off(self.instr.imm.value)

class s_STXA(SimInstr):
    def run(self):
        addr = self.instr.rsd.value
        val = self.instr.imm.value
        self.sim.ext[addr] = val

class s_CMPI(SimInstr):
    def run(self):
        ival = self.instr.imm.value 
        val = self.sim.get_reg(self.instr.ra.value)
        print(self.instr.operands)
        print(ival,val,ival-val)
        out = val-ival
        if out == 0:
            self.sim.z = 1
        else:
            self.sim.z = 0

class s_JNZ(SimInstr):
    def run(self):
        if self.sim.z == 0:
            print("jumping")
            print(self.sim.pc)
            self.sim.set_pc_off(self.instr.imm.value)
            print(self.sim.pc)
            

sim_map = {
        'MOVI':s_MOVI,
        'ADDI':s_ADDI,
        'J':s_J,
        'STXA':s_STXA,
        'CMPI':s_CMPI,
        'JNZ':s_JNZ,
        }


class Simulator:
    def __init__(self,size=512,reset=8,window=0,asm_file="asm/blink.asm"):
        self.assembler = Assembler()
        self.asm_file = asm_file
        self.mem = [0  for i in range(size)]
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


        # assemble the code
        txt = open(self.asm_file).read()
        self.assembler.parse(headers)
        self.assembler.parse(txt)
        self.out = self.assembler.assemble()
        for i,j in enumerate(self.out):
            self.mem[i] = j
    

    def set_pc_off(self,pos):
        self.pc = self.pc + pos

    def set_pc_abs(self,pos):
        self.pc = pos

    def get_reg(self,pos):
        assert pos >= 0 & pos < 8
        return self.mem[self.window+pos]

    def set_reg(self,pos,value):
        print(pos)
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
                print(cls_name," does not exist")
        val = self.mem[self.pc]
        print(val)
        if isinstance(val,SimInstr):
            val.run()

        self.pc += 1

if __name__ == "__main__":
    s = Simulator()
    for i in range(500):
        s.step()
    print(s)
