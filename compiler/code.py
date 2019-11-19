from registers import *
from boneless.arch.opcode import *


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


class Blinker(Firmware):
    def instr(self):
        delay = Delay()
        w = self.w
        w.req("delay")
        delay_count = 8192
        return [MOVI(w.delay, delay_count), delay(w.delay)]


if __name__ == "__main__":
    bl = Blinker()
    print(bl.code())

# 20191119 output ( reformatted )
c = [
    MOVI(R6, 4096),
    Label("main"),
    [MOVI(R0, 8192), [LD(R0, R6, -8), JAL(R7, "Delay")]],
    J("main"),
    Label("ExtraCode"),
    [
        [
            Label("Delay"),
            LDW(R6, -8),
            AND(R0, R1, R1),
            Label("_2666359660_again"),
            SUBI(R1, R1, 1),
            CMP(R0, R1),
            BZ("_2666359660_exit"),
            J("_2666359660_again"),
            Label("_2666359660_exit"),
            ADJW(8),
            JR(R7, 0),
        ]
    ],
]
