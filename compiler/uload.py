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
                LDXA(w.status, self.io_map.rx_status),  # load the RX status from the serial port
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

class Blinker:
    def __init__(self):
        pass


class FakeIO:
    rx_status = 1

class uLoader(Firmware):
    def instr(self):
        w = self.w
        w.req("rx")
        SubR.io_map = FakeIO()
        s = Serial()
        return [s.read(w.rx), s.write(w.rx)]


ul = uLoader()
c = ul.show()
