from .registers import *
from boneless.arch.opcode import *
from boneless.arch.asm import Assembler
import pprint


class Serial:

    class ReadBlock(SubR):
        def setup(self):
            self.locals = ["rx_status","counter","leds"]
            self.ret = ["char"]

        def instr(self):
            w = self.w
            ll = LocalLabels()
            rx_status = self.io_map.rx_status
            rx_data = self.io_map.rx_data
            return [
                MOVI(w.leds,1),
                MOVI(w.counter,0xFFFF),
                ll("rxdown"),
                Rem("load the RX status from the serial port"),
                [
                    SUBI(w.counter,w.counter,1),
                    CMPI(w.counter,0),
                    BEQ(ll.blink),
                    J(ll.next),
                    ll('blink'),
                    STXA(w.leds,self.io_map.led),
                    MOVI(w.counter,0xFFFF),
                    XORI(w.leds,w.leds,0xFFFF),
                ],
                LDXA(w.rx_status, rx_status),  # load the RX status from the serial port
                CMPI(w.rx_status, 1),  # compare the register to 1
                BEQ(ll.rxwait),  # if it is equal to zero continue
                ll('next'),
                J(ll.rxdown),
                LDXA(w.char, rx_data), # load the rx data into w.char
                MOVI(w.rx_status,1),
                STXA(w.rx_status,rx_status), # ack the char
                ll("rxwait"), # wait for the serial port to be ready
                LDXA(w.rx_status,rx_status),
                CMPI(w.rx_status,0),
                BEQ(ll.rxack),
                J(ll.rxwait),
                ll("rxack"),
                MOVI(w.rx_status,0),
                STXA(w.rx_status,rx_status), # ack the char
                MOVI(w.leds,0),
                STXA(w.leds,self.io_map.led),
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
                Rem('high byte'),
                OR(w.holding,w.holding,w.first),
                SRLI(w.holding,w.holding,8),
                Rem('low byte'),
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
                Rem('write high byte'),
                MOV(w.holding,w.word),
                SRLI(w.holding,w.holding,8),
                ww(w.holding),
                Rem('write low byte'),
                ANDI(w.holding,w.word,0x00FF),
                ww(w.holding),
            ]


    read = ReadBlock()
    write = Write()
    writeword = WriteWord()
    readword =  ReadWord()

class Blinker:
    class Blink(SubR):
        def setup(self):
            self.params = ["counter"]
            self.locals = ["leds"]

        def instr(self):
            w = self.w
            ll = LocalLabels()
            return [
                    ll('next'),
                    SUBI(w.counter,w.counter,1),
                    CMPI(w.counter,0),
                    BEQ(ll.blink),
                    J(ll.next),
                    ll('blink'),
                    STXA(w.leds,self.io_map.led),
                    XORI(w.leds,w.leds,0xFFFF),
                ]

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
        ll = LocalLabels()
        s = Serial()
        bl = Blinker()
        cs = CheckSum()
        wm = WriteToMem()
        return [
            MOVI(w.counter,5),
            ll('fnord'), 
            bl.blink(w.counter),
            ADDI(w.counter,w.counter,1),
            J(ll.fnord),
            #s.read(ret=w.current_value),
            #MOVI(w.current_value,ord('!')),
            #s.write(w.current_value),
        ]
        """
            Rem('load the starting address'),
            MOVR(w.address,'program_start'),
            ADDI(w.address,w.address,1),
            Rem('read the program length'),
            s.readword(ret=w.counter),
            s.writeword(w.counter),
            Rem('loop through the words'),
            ll('again'),
            [
                s.readword(ret=w.current_value),
                cs(w.char,w.checksum,ret=w.checksum),
                wm(w.current_value,w.address,ret=w.address),
                s.writeword(w.checksum),
            ],
            SUBI(w.counter,w.counter,1),
            CMPI(w.counter,0),
            BEQ(ll.boot_into),
            J(ll.again),
            ll('boot_into'),
            Rem('Boot into the new program'),
            ADJW(-8),
            MOVR(w.ret,'program_start'),
            JR(w.ret,1),
        ]
        """

if __name__ == "__main__":
    ul = uLoader(io_map=FakeIO())
    ul.show()
    fw = ul.assemble()
    from loader import load
    load(fw)
