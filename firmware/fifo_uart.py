from .registers import *
from boneless.arch.opcode import *
from boneless.arch.asm import Assembler

__all__ = ["Serial"]


class Serial:
    class ReadBlock(SubR):
        def setup(self):
            self.locals = ["rx_status", "counter", "leds"]
            self.ret = ["char"]

        def instr(self):
            w = self.w
            ll = LocalLabels()
            rx_status = self.io_map.rx_status
            rx_data = self.io_map.rx_data
            return [
                MOVI(w.leds, 1),
                MOVI(w.counter, 0xFFFF),
                ll("checkrx"),
                Rem("load the RX status from the serial port"),
                [
                    SUBI(w.counter, w.counter, 1),
                    CMPI(w.counter, 0),
                    BEQ(ll.blink),
                    J(ll.next),
                    ll("blink"),
                    STXA(w.leds, self.io_map.led),
                    MOVI(w.counter, 0xFFFF),
                    XORI(w.leds, w.leds, 0xFFFF),
                    ll("next"),
                ],
                LDXA(w.rx_status, rx_status),  # load the RX status from the serial port
                CMPI(w.rx_status, 1),  # compare the register to 1
                BEQ(ll.rxnext),  # if it is equal to zero continue
                J(ll.checkrx),
                ll("rxnext"),  # wait for the serial port to be ready
                LDXA(w.char, rx_data),  # load the rx data into w.char
                MOVI(w.rx_status, 1),
                STXA(w.rx_status, rx_status),  # write to the enable strobe to move data into the register
                MOVI(w.rx_status, 0),
                STXA(w.rx_status, rx_status),  # and drop the enable
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
                STXA(w.char, tx_data),  # put the holding data into the serial port
                MOVI(w.status, 1),  # set status to one
                STXA(w.status, tx_status),  # write to tx status
                MOVI(w.status, 0),  # set the status to zero
                STXA(w.status, tx_status),  # acknowledge the write
            ]

    class ReadWord(SubR):
        def setup(self):
            self.locals = ["first", "second", "holding"]
            self.ret = ["word"]

        def instr(self):
            w = self.w
            rb = Serial.read
            return [
                MOVI(w.holding, 0),
                Rem("low byte"),
                rb(ret=w.first),
                MOV(w.word, w.first),
                Rem("high byte"),
                rb(ret=w.second),
                MOV(w.holding, w.second),
                SLLI(w.holding, w.holding, 8),
                OR(w.word, w.word, w.holding),
            ]

    class WriteWord(SubR):
        def setup(self):
            self.params = ["word"]
            self.locals = ["holding", "extra"]

        def instr(self):
            w = self.w
            ww = Serial.Write()
            return [
                Rem("write high byte"),
                SRLI(w.holding, w.word, 8),
                ww(w.holding),
                Rem("write low byte"),
                ANDI(w.holding, w.word, 0x00FF),
                ww(w.holding),
            ]

    read = ReadBlock()
    write = Write()
    writeword = WriteWord()
    readword = ReadWord()
