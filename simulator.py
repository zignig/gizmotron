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
    def run(self):
        pass

class s_movi(SimInstr,MOVI):
    def run(self):
        print('fnord')


class Simulator:
    def __init__(self,size=512,reset=8,window=0,asm_file="asm/blink.asm"):
        self.assembler = Assembler()
        self.asm_file = asm_file
        self.mem = [0  for i in range(size)]
        self.size = size
        self.reset = reset
        self.windows = window
        self.pc = reset 

        # assemble the code
        txt = open(self.asm_file).read()
        self.assembler.parse(headers)
        self.assembler.parse(txt)
        self.out = self.assembler.assemble()
        for i,j in enumerate(self.out):
            self.mem[i] = j
    

    def step(self):
        val = self.mem[self.pc]
        # if it is an it , convert to an instruction
        if isinstance(val,int):
            instr = self.assembler.disassemble([val])[0]
            print(instr.__class__.__name__)
            self.mem[self.pc] = instr
        self.pc += 1

if __name__ == "__main__":
    s = Simulator()
    for i in range(10):
        s.step()
    print(s)
