# first cut of boneless simlator

from boneless.arch.asm import Assembler
from boneless.arch.opcode import * 
from boneless.arch.opcode import Instr 

from .simi import SimInstr
import .sopcodes

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
class Disconnected(BaseException):
    pass

# connect to external simulation objects
class External:
    def __init__(self,size):
        self.mem = []
        for i in range(size):
           self.mem.append(0)
        pass


    def __getitem__(self,key):
        print("external get:=",key)
        return self.mem[key]

    def __setitem__(self,key,value):
        print("external set:=",key,',',value)
        self.mem[key] = value

class Memory:
    def __init__(self,size):
        self.mem = []
        for i in range(size):
           self.mem.append(0)
    
 
    def __getitem__(self,key):
        return self.mem[key]

    def __setitem__(self,key,value):
        self.mem[key] = value

    def __repr__(self):
        s = ""
        for i,j in enumerate(self.mem):
            s += '{:04x}'.format(i)+' : '+str(j)+'\n'
        return s

class Simulator:
    def __init__(self,size=200,reset=8,window=0,asm_file="../asm/echo.asm"):
        self.assembler = Assembler()
        self.asm_file = asm_file
        self.size = size
        self.pc_reset = reset
        self.window_reset = window
        self.window = window
        self.pc = reset 
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
        # create memory and load the code
        self.mem = Memory(len(self.out)) 
        self.ext = External(20)
        for i,j in enumerate(self.out):
            self.mem[i] = j  
    
        # current instruction
        self.current = None
        self.debug = True 

    def reset(self):
        self.pc = self.pc_reset
        self.window = self.window_reset

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
    def R0(self):
        pass

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
    s.run(50)
