from .registers import *
from boneless.arch.opcode import *
from boneless.arch.asm import Assembler
import pprint
from .uart import Serial
from .leds import Blinker
from .lister import register


class CheckSum(SubR):
    def setup(self):
        self.params = ["data", "checksum"]
        self.locals = ["calc"]
        self.ret = ["checksum"]

    def instr(self):
        w = self.w
        return [
            SLLI(w.data, w.data, 1), 
            XOR(w.checksum, w.checksum, w.data)
        ]

class WriteToMem(SubR):
    def setup(self):
        self.params = ["data","address"]
        self.ret = ['address']
    
    def instr(self):
        w = self.w
        return [
                ST(w.data,w.address,0),
                ADDI(w.address,w.address,1)
        ]


def zero_registers(w):
    instr = []
    instr += [MOVI(w.ret,0)]
    for i in range(8,0,-1):
        instr += [ST(w.ret,w.fp,-i)]
    return instr

class FakeIO:
    rx_data = 0
    rx_status = 1
    leds = 2
    tx_data = 3
    tx_status = 4
    led = 5

@register
class uLoader(Firmware):
    def instr(self):
        w = self.w
        w.req("current_value")
        w.req("counter")
        w.req("checksum")
        w.req("address")
        ll = LocalLabels()
        s = Serial()
        bl = Blinker()
        cs = CheckSum()
        wm = WriteToMem()
        return [
            Rem('read the program length'),
            MOVR(w.address,"program_start"),
            ADDI(w.address,w.address,1),
            s.readword(ret=w.counter),
            s.writeword(w.counter),
            Rem('loop through the words'),
            ll('again'),
            [
                s.readword(ret=w.current_value),
                wm(w.current_value,w.address,ret=w.address),
                #cs(w.current_value,w.checksum,ret=w.checksum),
                s.writeword(w.current_value),
            ],
            SUBI(w.counter,w.counter,1),
            CMPI(w.counter,0),
            BEQ(ll.boot_into),
            J(ll.again),
            ll('boot_into'),
            Rem('Boot into the new program'),
            zero_registers(w),
            ADJW(-8),
            MOVR(w.ret,'program_start'),
            JR(w.ret,1),
        ]

if __name__ == "__main__":
    ul = uLoader(io_map=FakeIO())
    ul.show()
    fw = ul.assemble()
    from loader import load
    load(fw)
