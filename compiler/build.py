
import parser
import registers

from boneless.arch.asm import Assembler
from boneless.arch.opcode import *


def go(val):
    print(val)
    return val


class Program:
    def __init__(self, file_name="test.prg"):
        self.file_name = file_name
        self.result = parser.parse(self.file_name)
        self.sections = self.result.sections
        self.declarations = self.result.declarations
        self.variables = self.result.variables
        self.assembler = Assembler()

    def build(self):
        code = []
        for i in p.sections:
            code.append(list(p.sections[i].build()))
        for i in p.declarations:
            code.append(list(p.declarations[i].make()))
        for i in code:
            print(i)
        
        self.code = code
        self.assembler.parse(code)

        r = self.assembler.assemble()
        print(r)
        print(len(r))


p = Program()
p.build()
