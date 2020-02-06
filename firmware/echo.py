from .registers import *
from boneless.arch.opcode import *
from boneless.arch.asm import Assembler
import pprint
from .uart import Serial
from .leds import Blinker

class echo(Firmware):
    def instr(self):
        w = self.w
        w.req("current_value")
        ll = LocalLabels()
        s = Serial()
        return [
            s.read(ret=w.current_value),
            s.write(w.current_value),
        ]
