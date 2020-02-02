from registers import *
from boneless.arch.opcode import *
from boneless.arch.asm import Assembler
import pprint


class Serial():
    class ReadBlock(SubR):
        def setup(self):
            self.params = ["char"]
            self.locals = ["counter", "status", "rx_status"]

        def instr(self):
            w = self.w
            ll = LocalLabels()
            return [
                ll("rxdown"),
                LDXA(
                    w.status, self.io_map.rx_status
                ),  # load the RX status from the serial port
                CMPI(w.status, 1),  # compare the register to 1
                BEQ(ll.rxcont),  # if it is equal to zero continue
                J(ll.rxdown),
                ll("rxcont"),
            ]

    class Write(SubR):
        def setup(self):
            self.params = ["char"]
            self.locals = ["status"]

        def instr(self):
            w = self.w
            ll = LocalLabels()
            return []

    read = ReadBlock()
    write = Write()


class Blinker():
    class Blink(SubR):
        def setup(self):
            self.params = ["value", "next"]

        def instr(self):
            w = self.w
            return [STXA(w.value, self.io_map.leds)]

    def make(self):
        self.blink = self.Blink()

    blink = Blink()

class CheckSum(SubR):
    def setup(self):
        self.params = ["data","checksum"]
        self.locals = ["calc"]

    def instr(self):
        w = self.w
        return [
            SRLI(w.data,w.data,1),
            XOR(w.data,w.checksum,w.data)
        ]
            
            
class FakeIO:
    rx_status = 1
    leds = 2


class uLoader(Firmware):
    def instr(self):
        w = self.w
        w.req("rx")
        w.req("led_val")
        w.req("led_next")
        w.req("checksum")
        # map the IO to all the Subroutines
        SubR.io_map = FakeIO()
        s = Serial()
        bl = Blinker()
        cs = CheckSum()
        return [
            s.read(w.rx), 
            bl.blink(w.led_val, w.led_next), 
            cs(w.rx,w.checksum),
            s.write(w.rx)
        ]


ul = uLoader()
c = ul.show()
ul.assemble()
