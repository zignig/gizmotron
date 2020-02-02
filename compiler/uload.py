from registers import *
from boneless.arch.opcode import *
from boneless.arch.asm import Assembler
import pprint


class Serial:
    class ReadBlock(SubR):
        def setup(self):
            self.locals = ["rx_status"]
            self.ret = ["char"]

        def instr(self):
            w = self.w
            ll = LocalLabels()
            rx_status = self.io_map.rx_status
            rx_data = self.io_map.rx_data
            return [
                ll("rxdown"),
                Rem("load the RX status from the serial port"),
                LDXA(w.rx_status, rx_status),  # load the RX status from the serial port
                CMPI(w.rx_status, 1),  # compare the register to 1
                BEQ(ll.rxcont),  # if it is equal to zero continue
                J(ll.rxdown),
                ll("rxcont"),
                LDXA(w.char, rx_data),
            ]

    class Write(SubR):
        def setup(self):
            self.params = ["char"]
            self.locals = ["status"]

        def instr(self):
            w = self.w
            ll = LocalLabels()
            tx_data = self.io_map.tx_data
            tx_status = self.io_map.tx_status
            return [
                ll("txchar"),  # put a char into the serial port
                STXA(w.char, tx_data),  # put the holding data into the serial port
                MOVI(w.status, 1),  # set status to one
                STXA(w.status, tx_status),  # write to tx status
                MOVI(w.status, 0),  # set the status to zero
                STXA(w.status, tx_status),  # acknowledge the write
                ll("waitup"),  # TODO , this should be a fifo in the serial port
                LDXA(w.status, tx_status),  # wait for tx status to go high
                CMPI(w.status, 1),
                BEQ(ll.waitup),
                ll("waitdown"),
                LDXA(w.status, tx_status),  # wait for the status to go low
                CMPI(w.status, 0),
                BEQ(ll.waitdown),
            ]

    read = ReadBlock()
    write = Write()


class Blinker:
    class Blink(SubR):
        def setup(self):
            self.params = ["value"]

        def instr(self):
            w = self.w
            return [STXA(w.value, self.io_map.leds)]

    blink = Blink()


class CheckSum(SubR):
    def setup(self):
        self.params = ["data", "checksum"]
        self.locals = ["calc"]
        self.ret = ["checksum"]

    def instr(self):
        w = self.w
        return [SRLI(w.data, w.data, 1), XOR(w.data, w.checksum, w.data)]


class FakeIO:
    rx_data = 0
    rx_status = 1
    leds = 2
    tx_data = 3
    tx_status = 4


class uLoader(Firmware):
    def instr(self):
        w = self.w
        w.req("current_value")
        w.req("char")
        w.req("led_val")
        w.req("checksum")
        w.req("address")
        # map the IO to all the Subroutines
        SubR.io_map = FakeIO()
        s = Serial()
        bl = Blinker()
        cs = CheckSum()
        return [
            s.read(ret=w.char),
            bl.blink(w.led_val),
            cs(w.char,w.checksum,ret=w.checksum),
            s.write(w.char)
        ]


ul = uLoader()
c = ul.show()
ul.assemble()
