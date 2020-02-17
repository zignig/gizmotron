from .registers import *
from boneless.arch.opcode import *
from boneless.arch.asm import Assembler
import pprint
from .uart import Serial
from .leds import Blinker
from .lister import register


class CheckSum(SubR):
    " running checksum code "
    # TODO convert to proper checksum
    def setup(self):
        self.params = ["data", "checksum"]
        self.locals = ["calc"]
        self.ret = ["checksum"]

    def instr(self):
        w = self.w
        return [SLLI(w.data, w.data, 1), XOR(w.checksum, w.checksum, w.data)]


class WriteToMem(SubR):
    " Write a data word to address and increment address"

    def setup(self):
        self.params = ["data", "address"]
        self.ret = ["address"]

    def instr(self):
        w = self.w
        return [ST(w.data, w.address, 0), ADDI(w.address, w.address, 1)]


class ProgramDump(SubR):
    "Dump a memory block onto the serial port"
    def setup(self):
        self.params = ["address","count"]
        self.locals = ["value"]

    def instr(self):
        w = self.w
        ll = LocalLabels()
        s = Serial()
        return [
                ll('again'),
                LD(w.value,w.address,0),
                s.writeword(w.value),
                ADDI(w.address,w.address,1),
                SUBI(w.count,w.count,1),
                CMPI(w.count,0),
                BEQ(ll.exit),
                J(ll.again),
                ll("exit"),
            ]

                
class WaitForQ(SubR):
    " wait for a question mark and write iD"

    def setup(self):
        self.ret = ["status"]
        self.locals = ["char", "id"]

    def instr(self):
        w = self.w
        ll = LocalLabels()
        s = Serial()
        return [
            ll("wait"),
            s.read(ret=w.char),
            CMPI(w.char, ord("?")),
            BEQ(ll.cont),
            J(ll.wait),
            ll("cont"),
            MOVI(w.status, 1),
            MOVI(w.id,0xDEAD),
            s.writeword(w.id),
            MOVI(w.id,0xBEEF),
            s.writeword(w.id),
        ]


def zero_registers(w):
    " blank all the registers in the frame above"
    instr = []
    instr += [MOVI(w.ret, 0)]
    for i in range(8, 0, -1):
        instr += [ST(w.ret, w.fp, -i)]
    return instr


class FakeIO:
    " fake io for testing"
    rx_data = 0
    rx_status = 1
    leds = 2
    tx_data = 3
    tx_status = 4
    led = 5


@register
class uLoader(Firmware):
    """
    send word length
    send words 
    should boot into program 

    
    """

    # TODO add in handshake , wait for "?" (63)
    # TODO send ID , 2 words
    def instr(self):
        w = self.w
        w.req("current_value")
        w.req("counter")
        w.req("checksum")
        w.req("address")
        w.req("prog_length")
        w.req("status")
        ll = LocalLabels()
        s = Serial()
        bl = Blinker()
        cs = CheckSum()
        wm = WriteToMem()
        wfq = WaitForQ()
        pd = ProgramDump()
        return [
            Rem('Wait for a question mark'),
            wfq(ret=w.status),
            Rem("read the program length"),
            MOVR(w.address, "program_start"),
            ADDI(w.address, w.address, 1),
            s.readword(ret=w.counter),
            s.writeword(w.counter),
            Rem("Copy the program length for later"),
            MOVI(w.counter,10),
            MOV(w.counter,w.prog_length),
            Rem("loop through the words"),
            ll("again"),
            [
                s.readword(ret=w.current_value),
                wm(w.current_value,w.address, ret=w.address),
                #cs(w.current_value, w.checksum, ret=w.checksum),
                s.writeword(w.counter),
            ],
            SUBI(w.counter, w.counter, 1),
            CMPI(w.counter, 0),
            BEQ(ll.boot_into),
            J(ll.again),
            ll("boot_into"),
            Rem("Boot into the new program"),

            #zero_registers(w),
            #ADJW(-8),
            #MOVR(w.ret, "program_start"),
            #JR(w.ret, 1),
            Rem("dump the program for testing and debugging"),
            MOVR(w.address, "program_start"),
            pd(w.address,w.prog_length),
            J('init'),
        ]


if __name__ == "__main__":
    ul = uLoader(io_map=FakeIO())
    ul.show()
    fw = ul.assemble()
    from loader import load

    load(fw)
