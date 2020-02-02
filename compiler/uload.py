from registers import *
from boneless.arch.opcode import *
from boneless.arch.asm import Assembler
import pprint


class LibR:
    def __init__(self):
        self.make()

    def make(self):
        raise


class Serial(LibR):
    class ReadBlock(SubR):
        def setup(self):
            self.params = ["char"]
            self.locals = ["counter", "status", "rx_status"]

        def instr(self):
            w = self.w
            ll = LocalLabels()
            print(dir(self))
            return [
                ll("rxdown"),
                LDXA(
                    w.status, self.io_map.rx_status
                ),  # load the RX status from the serial port
                CMPI(w.status, 0),  # compare the register to 1
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

    def make(self):
        self.read = self.ReadBlock()
        self.write = self.Write()


class Blinker(LibR):
    class Blink(SubR):
        def setup(self):
            self.params = ["value", "next"]

        def instr(self):
            w = self.w
            return [STXA(w.value, self.io_map.leds)]

    def make(self):
        self.blink = self.Blink()


class FakeIO:
    rx_status = 1
    leds = 2


class uLoader(Firmware):
    def instr(self):
        w = self.w
        w.req("rx")
        w.req("led_val")
        w.req("led_next")
        SubR.io_map = FakeIO()
        s = Serial()
        bl = Blinker()
        return [s.read(w.rx), bl.blink(w.led_val, w.led_next), s.write(w.rx)]


ul = uLoader()
c = ul.show()
