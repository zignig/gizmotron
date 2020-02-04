from registers import *
from boneless.arch.opcode import *
from boneless.arch.asm import Assembler

from collections import OrderedDict

class MatchTable(metaclass=MetaSub):
    " single char match and jump table"

    def __init__(self):
        self.table = OrderedDict()

    def add(self,char,label):
        if not ((type(char) == type('')) and (len(char)== 1)):
            raise ValueError("needs to be a char")
        self.table[ord(char)] = RR(label)


    def code(self):
        instr = []
        for i,j in self.table.items():
            instr.append([i,j])
        return instr


m = MatchTable()
m.add('a','test')
m.add('b','test2')

print(m.code()) 

    
            
        
