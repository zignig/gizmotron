# first cut of boneless simlator

from boneless.arch.asm import Assembler
from boneless.arch.opcode import * 
from boneless.arch.opcode import Instr 

from .simi import SimInstr
from .sopcodes import sim_dict

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

class zero:
    def read(self):
        return 0
    def write(self,val):
        return 0

class on:
    def read(self):
        return 1
    def write(self,val):
        return 1

class External:
    def __init__(self,size):
        self.mem = []
        for i in range(size):
            self.mem.append(on())

    def bind(self,reg):
        self.mem = reg

    def __getitem__(self,key):
        # TODO , bind to simulated registers in gizmo
        print("external get:=",key)
        print(self.mem[key].read())
        return self.mem[key].read()

    def __setitem__(self,key,value):
        # TODO , bind to simulated registers in gizmo
        print("external set:=",key,',',value)
        print(self.mem)
        self.mem[key].write(value)

class Memory:
    def __init__(self,size,sim):
        self.mem = []
        self.sim = sim
        for i in range(size):
           self.mem.append(0)
    
 
    def __getitem__(self,key):
        return self.mem[key]

    def __setitem__(self,key,value):
        self.mem[key] = value

    def __repr__(self):
        s = ""
        for i,j in enumerate(self.mem):
            if self.sim.pc == i:
                s += '>'
            s += '{:04x}'.format(i)+' : '+'{:>15s}'.format(str(j))+' | '
            if i % 5 == 4:
                s += '\n'
        return s

class Simulator:
    def __init__(self,size=200,reset=8,window=0,asm_file="../asm/echo.asm"):
        self.asm_file = asm_file
        self.size = size
        self.pc_reset = reset
        self.window_reset = window
        self.window = window
        self.pc = reset 
        self.counter = 0 
        # flags
        self.z = 0
        self.s = 0
        self.c = 0 
        self.v = 0

        self.has_exti = False
        self.exti_val = 0

        # current instruction
        self.current = None
        self.debug = True 
        self.load(asm_file)

        # external interface
        self.ext = External(20)
        # TODO bind gizmos to these values
        self.ext.mem[2] = on()

    def load(self,asm_file=''):
        self.assembler = Assembler()
        if asm_file != '':
           self.asm_file = asm_file
        # assemble the code
        txt = open(self.asm_file).read()
        self.assembler.parse(headers)
        self.assembler.parse(txt)
        self.out = self.assembler.assemble()
        # create memory and load the code
        self.mem = Memory(len(self.out),self) 
        for i,j in enumerate(self.out):
            self.mem[i] = j  
        self.pc = self.pc_reset 

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
            if cls_name in sim_dict:
                sim_instr = sim_dict[cls_name](instr,self)
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
        self.counter += 1

    @property
    def R0(self):
        pass

    @property
    def w(self):
        return self.mem[self.window:self.window+8]

    @property
    def fl(self):
        return [self.z,self.c]

    def run(self,count=1000000):
        for i in range(count):
            self.step()

if __name__ == "__main__":
    s = Simulator()
