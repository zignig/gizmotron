from registers import *
from boneless.arch.opcode import *
from boneless.arch.asm import Assembler
import pprint


class Adder(SubR):
    def setup(self):
        self.params = ["left","right"]
        self.ret = ["sum"]

    def instr(self):
        w = self.w
        return [
                ADD(w.sum,w.left,w.right),
        ]

adder = Adder()
w = Window()
w.req(['a','b','c'])
code = [adder(w.a,w.b,ret=w.c),MetaSub.code()]
pprint.pprint(code,width=1,indent=3)
