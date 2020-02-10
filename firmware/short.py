from registers import *
from boneless.arch.opcode import *
from boneless.arch.asm import Assembler
import pprint


class Adder(SubR):
    def setup(self):
        self.params = ["left", "right"]
        self.ret = ["sum"]

    def instr(self):
        w = self.w
        return [ADD(w.sum, w.left, w.right)]


class Short(Firmware):
    def instr(self):
        adder = Adder()
        w = self.w
        w.req(["a", "b", "c"])
        return [adder(w.a, w.b, ret=w.c)]


if __name__ == "__main__":
    ul = Short()
    fw = ul.assemble()
    ul.show()
    from loader import load

    load(fw)
