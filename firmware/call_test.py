from .registers import *
from boneless.arch.opcode import *
from boneless.arch.asm import Assembler
from .lister import register


class Depth1(SubR):
    def instr(self):
        return [ADDI(R0, R0, 1)]


class Depth2(SubR):
    def instr(self):
        return [Depth1()()]


class Depth3(SubR):
    def instr(self):
        return [Depth2()()]


class Recurse(SubR):
    def setup(self):
        self.params = ["value", "counter"]
        self.ret = ["value", "counter"]

    def instr(self):
        w = self.w
        ll = LocalLabels()
        recurse = Recurse()
        return [
            Rem("decrement the counter, stop @ zero"),
            ADDI(w.value, w.value, 10),
            SUBI(w.counter, w.counter, 1),
            CMPI(w.counter, 0),
            BEQ(ll.exit),
            recurse(w.value, w.counter, ret=[w.value, w.counter]),
            ll("exit"),
        ]


@register
class Caller(Firmware):
    def instr(self):
        w = self.w
        w.req(["value", "counter"])
        ll = LocalLabels()
        r = Recurse()
        return [
            C("depth", 3),
            MOVI(w.value, 1000),
            ll("again"),
            MOVI(w.counter, "depth"),
            r(w.value, w.counter, ret=[w.value]),
            J(ll.again),
        ]
