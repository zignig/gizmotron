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


    class ReadWord(SubR):
        def setup(self):
            self.locals = ["first","second","holding"]
            self.ret = ["word"]

        def instr(self):
            w = self.w
            rb = Serial.read
            return [
                rb(ret=w.first),
                rb(ret=w.second),
                MOVI(w.holding,0),
                OR(w.holding,w.holding,w.first),
                SRLI(w.holding,w.holding,8),
                OR(w.holding,w.holding,w.second)
            ]


    class WriteWord(SubR):
        def setup(self):
            self.params = ["word"]
            self.locals = ["holding"]

        def instr(self):
            w = self.w
            ww = Serial.Write()
            return [
                ANDI(w.holding,w.word,0x00FF),
                ww(w.holding),
                MOV(w.holding,w.word),
                SRLI(w.holding,w.holding,8),
                ww(w.holding),
            ]


    read = ReadBlock()
    write = Write()
    writeword = WriteWord()
    readword =  ReadWord()

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
        w.req("counter")
        w.req("checksum")
        w.req("address")
        # map the IO to all the Subroutines
        SubR.io_map = FakeIO()
        s = Serial()
        bl = Blinker()
        cs = CheckSum()
        wm = WriteToMem()
        return [
            Rem('load the starting address'),
            MOVR(w.address,'program_start'),
            ADDI(w.address,w.address,1),
            Rem('read the program length'),
            s.readword(ret=w.counter),
            Rem('loop through the words'),
            L('again'),
            [
                s.readword(ret=w.current_value),
                cs(w.char,w.checksum,ret=w.checksum),
                wm(w.current_value,w.address,ret=w.address),
                s.writeword(w.checksum),
            ],
            SUBI(w.counter,w.counter,1),
            CMPI(w.counter,0),
            BEQ('boot_into'),
            J('again'),
            L('boot_into'),
            Rem('Boot into the new program'),
            ADJW(-8),
            MOVR(w.ret,'program_start'),
            JR(w.ret,1),
        ]

#SubR.debug = False
#ul = uLoader()
#c = ul.show()
if False:
    code = ul.assemble()
    a = Assembler()
    di = a.disassemble(code)
    pprint.pprint(di)

def b16(i): return '{:016b}'.format(i)
def b8(i): return '{:08b}'.format(i)
if __name__ == "__main__":
    ul = uLoader()
    fw = ul.assemble()
    for i in fw:
        print(b16(i),b8(i >> 8),b8(i & 0xFF))
