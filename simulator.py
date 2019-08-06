# first cut of boneless simlator

from boneless.arch.asm import Assembler

class Simulator:
    def __init__(self,size=512,reset=9,window=0,asm_file="asm/blink.asm"):
        self.assembler = Assembler()
        self.file_name = asm_file
        self.mem = [0  for i in range(size)]
        self.size = size
        self.reset = reset
        self.windows = window
        self.pc = reset 

    

if __name__ == "__main__":
    s = Simulator()
    print(s)
