from registers import * 
from boneless.arch.opcode import *

class Delay(SubR):
    def setup(self):
        self.params = ['duration']
        self.locals = ['counter']

    def instr(self):
        w = self.w
        ll = LocalLabels()
        return [
            MOV(w.duration,w.counter),
            ll('again'),
            SUBI(w.counter,w.counter,1),
            CMP(w.duration,w.counter),
            BZ(ll.exit),
            J(ll.again),
            ll('exit'),
        ]


class Blinker(Firmware):
    def instr(self):
        delay = Delay()
        w = self.w
        w.req('delay')
        delay_count = 8192
        return [
            MOVI(w.delay,delay_count),
            delay(w.delay),
        ]

if __name__ == "__main__":
    bl = Blinker()
    print(bl.code())
