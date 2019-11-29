from registers import *
from boneless.arch.opcode import *
import pprint


class Delay(SubR):
    def setup(self):
        self.params = ["duration"]
        self.locals = ["counter"]

    def instr(self):
        w = self.w
        ll = LocalLabels()
        return [
            MOV(w.duration, w.counter),
            ll("again"),
            SUBI(w.counter, w.counter, 1),
            CMP(w.duration, w.counter),
            BZ(ll.exit),
            J(ll.again),
            ll("exit"),
        ]


class Writer(SubR):
    def setup(self):
        self.params = ["address","count","target"]
        self.locals = ["val","pos","finish"]

    def instr(self):
        w = self.w
        ll = LocalLabels()
        return [
                MOV(w.pos,w.address),
                MOV(w.finish,w.address),
                ADD(w.finish,w.finish,w.count),
                ll("again"),
                MOVR(w.val,w.pos),
                STXA(w.val,w.target),
                ADDI(w.pos,w.pos,1),
                CMP(w.pos,w.finish),
                BZ(ll.exit),
                J(ll.again),
                ll('exit'),
        ]

class Leds(SubR):
    def setup(self):
        self.params = ["value"]

    def instr(self):
        return [STXA(self.w.value, 1)]


class Blinker(Firmware):
    def instr(self):
        delay = Delay()
        leds = Leds()
        writer = Writer()
        w = self.w
        w.req("delay")
        w.req("counter")
        w.req("address")
        w.req("count")
        w.req("target")
        delay_count = 8192
        return [
            MOVI(w.delay, delay_count),
            delay(w.delay),
            ADDI(w.counter, w.counter, 1),
            leds(w.counter),
            MOVI(w.address,5),
            MOVI(w.count,40),
            writer(w.address,w.count,w.target)
        ]

if __name__ == "__main__":
    bl = Blinker()
    pprint.pprint(bl.code(), indent=4)
