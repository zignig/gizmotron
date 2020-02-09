from .registers import *
from boneless.arch.opcode import *
from boneless.arch.asm import Assembler
import pprint
from .uart import Serial
from .leds import Blinker

from .lister import register


@register
class Echo(Firmware):
    def instr(self):
        w = self.w
        w.req("current_value")
        ll = LocalLabels()
        s = Serial()
        return [
            #s.read(ret=w.current_value),
            #s.write(w.current_value),
            s.readword(ret=w.current_value),
            s.writeword(w.current_value),
        ]
