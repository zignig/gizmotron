from .registers import *
from boneless.arch.opcode import *
from boneless.arch.asm import Assembler
from .lister import register


class Time:
    class Wait(SubR):
        def setup(self):
            self.params = ["count"]
            self.ret = ["loop", "counter"]
            self.size = 200

        def instr(self):
            w = self.w
            ll = LocalLabels()
            return [
                MOVI(w.counter,self.size),
                ll("again"),
                SUBI(w.counter, w.counter, 1),
                CMPI(w.counter, 0),
                BEQ(ll.step),
                J(ll.again),
                ll("step"),
                MOVI(w.counter, self.size),
                SUBI(w.count,w.count,1),
                CMPI(w.count,0),
                BEQ(ll.exit),
                J(ll.again),
                ll("exit"),
            ]
    
    wait = Wait()
