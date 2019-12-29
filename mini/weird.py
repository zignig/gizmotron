from nmigen import *
from core import CPU, MetaInstr, Instr, PC, ProgramCounter
from mem import RAM
from stack import Stack


class Weird(CPU):
    states = ["fetch", "decode", "load1", "load2", "wait", "execute"]

    class switch(PC):
        pc = ProgramCounter(0)

        def decode(self, m):
            pass

        def load1(self):
            pass

    class dstack(Instr):
        ds = Stack()

        def device(self):
            return self.ds

    class rstack(Instr):
        rs = Stack()

        def device(self):
            return self.rs

    class rpop(rstack):
        pass

    class fpstack(Instr):
        fp = Stack(width=64)

        def device(self):
            return self.fp

    class mem(Instr):
        r = RAM()

        def device(self):
            return self.r

        def fetch(self):
            pass

    class ref(Instr):
        r = RAM()

        def device(self):
            return self.r

    class store(Instr):
        s = RAM()

        def device(self):
            return self.s

    class incoming(Instr):
        def fetch(self):
            pass

        def execute(self):
            pass


h = Weird()
h.show()
