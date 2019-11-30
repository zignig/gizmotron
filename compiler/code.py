from registers import *
from boneless.arch.opcode import *
from boneless.arch.asm import Assembler
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
        return [STXA(self.w.value, 0)]


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
        ]


if __name__ == "__main__":
    bl = Blinker()
    code = bl.code()
    pprint.pprint(code)
    asm = Assembler()
    asm.parse(code)
    bin = asm.assemble()
    print(bin)

"""
[MOVI(R6, 4096),
 Label('main'),
 [MOVI(R0, 8192),
  [LD(R0, R6, -8), JAL(R7, 'Delay')],
  [LD(R1, R6, -8), JAL(R7, 'LedSet')],
  ADDI(R1, R1, 1)],
 J('main'),
 Label('ExtraCode'),
 [[Label('Delay'),
   LDW(R6, -8),
   AND(R0, R1, R1),
   Label('again_419233995'),
   SUBI(R1, R1, 1),
   CMP(R0, R1),
   BZ('exit_419233995'),
   J('again_419233995'),
   Label('exit_419233995'),
   ADJW(8),
   JR(R7, 0)],
  [Label('LedSet'), LDW(R6, -8), STXA(R0, 0), ADJW(8), JR(R7, 0)]]]
[49664, 34304, 50176, 32768, 16600, 44804, 16856, 44810, 6433, 49144, 42616, 33, 6449, 25, 47105, 49148, 41032, 42880, 42616, 30720, 41032, 42880]
"""
=======
            ADDI(w.counter, w.counter, 1),
            leds(w.counter),
            MOVI(w.address,5),
            MOVI(w.count,40),
            writer(w.address,w.count,w.target)
        ]

if __name__ == "__main__":
    bl = Blinker()
    pprint.pprint(bl.code(), indent=4)
>>>>>>> 7ade2ebf26d42bc59562daf99ad09007bbbae911
