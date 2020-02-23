from .registers import *
from boneless.arch.opcode import *
from boneless.arch.asm import Assembler
import pprint
from .leds import Blinker

from .lister import register

#from .fifo_uart import Serial
from .uart import Serial
from .time import Time

@register
class Echo(Firmware):
    def instr(self):
        w = self.w
        w.req(["current_value","write_value","wait_count"])
        ll = LocalLabels()
        s = Serial()
        t = Time()
        return [
            #MOVI(w.wait_count,30),
            #t.wait(w.wait_count), 
            #ll("again"),
            s.read(ret=w.current_value),
            s.write(w.current_value),
            #J(ll.again),
            #s.readword(ret=w.current_value),
            #s.writeword(w.current_value),
        ]
