from .registers import *
from boneless.arch.opcode import *
from .lister import register


class Blinker:
    class Blink(SubR):
        def setup(self):
            self.locals = ["counter", "leds"]

        def instr(self):
            w = self.w
            ll = LocalLabels()
            return [
                MOVI(w.counter, 0xFFFF),
                ll("next"),
                SUBI(w.counter, w.counter, 1),
                CMPI(w.counter, 0),
                BEQ(ll.blink),
                J(ll.next),
                ll("blink"),
                STXA(w.leds, self.io_map.led),
                XORI(w.leds, w.leds, 0xFFFF),
            ]

    blink = Blink()


@register
class Blinky(Firmware):
    def instr(self):
        w = self.w
        ll = LocalLabels()
        w.req("counter")
        w.req("leds")
        return [
            MOVI(w.counter, 32000),
            ll("next"),
            SUBI(w.counter, w.counter, 1),
            CMPI(w.counter, 0),
            BEQ(ll.blink),
            J(ll.next),
            ll("blink"),
            STXA(w.leds, self.io_map.led),
            XORI(w.leds, w.leds, 0xFFFF),
        ]
