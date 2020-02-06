from registers import *
from boneless.arch.opcode import *
from .uart import Serial


class Stringer(Block):
    class WriteString(SubR):
        def setup(self):
            self.params = ["address"]
            self.locals = ["length","finish","char"]

        def instr(self):
            w = self.w
            ll = LocalLabels()
            w = Serial()
            return [
                LD(w.length,w.address,0),
                CMPI(w.length,0),
                Rem('empty string continue'),
                BEQ(ll.exitdump),
                Rem("calculate the end of the string"),
                ADD(w.finish,w.address,w.length),
                ll("nextchar"),
                ADDI(w.address,w.address,1),
                LD(w.char,w.address,0),
                w.write(w.char),
                CMP(w.address,w.finish),
                BLTU(ll.nextchar),
                ll("exitdump"),
            ]
    writestring = WriteString()
