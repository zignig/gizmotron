# first cut of boneless simlator

from boneless.arch.asm import Assembler
from boneless.arch.opcode import * 
from boneless.arch.opcode import Instr 

from simi import SimInstr
import sopcodes

sim_map = sopcodes.sim_dict
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

class Simulator:
    def __init__(self,size=200,reset=8,window=0,asm_file="../asm/sim_test.asm"):
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
        self.exti_val = 0

        # assemble the code
        txt = open(self.asm_file).read()
        self.assembler.parse(headers)
        self.assembler.parse(txt)
        self.out = self.assembler.assemble()
        for i,j in enumerate(self.out):
            self.mem.append(j)
    
        # current instruction
        self.current = None
        self.debug = False 

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

        if self.debug:
            print(self.pc,self.w,self.current,self.fl)
        if isinstance(val,SimInstr):
            val.call()
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
    s.run(1000)
