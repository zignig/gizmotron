from .registers import *
from boneless.arch.opcode import *

class Blinker:
    class Blink(SubR):
        def setup(self):
            self.params = ["counter"]
            self.locals = ["leds"]

        def instr(self):
            w = self.w
            ll = LocalLabels()
            return [
                    ll('next'),
                    SUBI(w.counter,w.counter,1),
                    CMPI(w.counter,0),
                    BEQ(ll.blink),
                    J(ll.next),
                    ll('blink'),
                    STXA(w.leds,self.io_map.led),
                    XORI(w.leds,w.leds,0xFFFF),
                ]

    blink = Blink()
