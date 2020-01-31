from registers import *
from boneless.arch.opcode import *
from boneless.arch.asm import Assembler
import pprint

class Serial:
    class Read(SubR):
        def setup(self):
            self.params = ["duration"]
            self.locals = ["counter"]
            self.ret = ["status"]

        def instr(self):
            w = self.w
            ll = LocalLabels()
            return [
                    ADDI(w.counter,w.counter,1)
                   ]

    class Sub(SubR):
        pass

    read = Read()
    sub = Sub()

w = Window()
w.req('test')
s =Serial()
s.read(w.test)
s.sub()

class uLoader(Firmware):
    pass


MetaSub.code()
