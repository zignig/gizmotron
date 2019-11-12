
import parser
import registers

from boneless.arch.asm import Assembler
from boneless.arch.opcode import *


def go(val):
    print(val)
    return val


class Program:
    def __init__(self, file_name="test.prg", debug=False):
        self.file_name = file_name
        self.result = parser.parse(self.file_name, debug=debug)
        self.sections = self.result.sections
        self.declarations = self.result.declarations
        self.variables = self.result.variables
        self.assembler = Assembler()

    def show(self):
        self.result.show()

    def build(self):
        self.result.eval()
        self.show()
        return
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
        # print(r)
        # print(len(r))


p = Program(debug=False)
p.build()
