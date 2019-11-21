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


class LedSet(SubR):
    def setup(self):
        self.params = ["value"]

    def instr(self):
        return [STXA(self.w.value, 0)]


class Blinker(Firmware):
    def instr(self):
        delay = Delay()
        ledset = LedSet()
        w = self.w
        w.req("delay")
        w.req("lednum")
        delay_count = 8192
        return [
            MOVI(w.delay, delay_count),
            delay(w.delay),
            ledset(w.lednum),
            ADDI(w.lednum, w.lednum, 1),
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
