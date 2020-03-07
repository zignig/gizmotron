# morse encoder

from nmigen import *
from nmigen.cli import pysim
from nmigen.hdl.rec import Layout
import stream

# coding is 16 bits
# XXXXXX.....ngyyy
# X : dots and dashes
# . : undefined ( as yet )
# n : no encoding
# g : word gap
# y : length of code
import math

debug = True


def power_of_2(x):
    return 1 if x == 0 else math.ceil(math.log2(x))


coding = {
    "A": ".-",
    "B": "-...",
    "C": "-.-.",
    "D": "-..",
    "E": ".",
    "F": "..-.",
    "G": "--.",
    "H": "....",
    "I": "..",
    "J": ".---",
    "K": "-.-",
    "L": ".-..",
    "M": "--",
    "N": "-.",
    "O": "---",
    "P": ".--.",
    "Q": "--.-",
    "R": ".-.",
    "S": "...",
    "T": "-",
    "U": "..-",
    "V": "...-",
    "W": ".--",
    "X": "-..-",
    "Y": "-.--",
    "Z": "--..",
    "0": "-----",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
    ".": ".-.-.-",
    ",": "--..--",
    ":": "---...",
    "?": "..--..",
    "'": ".----.",
    "-": "-....-",
    '"': ".-..-.",
    "@": ".--.-.",
    "=": "-...-",
    " ": "_",
}

# morse constants
class morse_const:
    dit_length = 1
    dah_length = 3
    symbol_gap = 1
    letter_gap = 3
    word_gap = 3 # actually 7 has a letter gap


# encode the morse into binary


def convert(coding):
    max = 0
    min_c = 10000
    max_c = 0

    for i, j in coding.items():
        if debug:
            print(ord(i), i, j, len(j))
        # get the max length
        if len(j) > max:
            max = len(j)
        if ord(i) < min_c:
            min_c = ord(i)
        if ord(i) > max_c:
            max_c = ord(i)
    if debug:
        print(min_c, max_c)
        print(max_c - min_c)
    if debug:
        print("MAX ", max, power_of_2(max))
    d = {}
    for i, j in coding.items():
        num = encode(i, j, max)
        d[ord(i)] = num
    return d


def as_bits(i):
    return "{:016b}".format(i)


def zero_pad(l):
    pad = "".join(["0" for j in range(l)])
    return pad


def encode(letter, code, max):
    " encode a letter into binary"
    l = len(code)
    s = ""
    gap = False
    # encode the bits
    for i in code:
        if i == ".":
            s += "0"
        if i == "-":
            s += "1"
        if i == "_":
            l = 1
            gap = True
    # pad to max length
    pad = "".join(["0" for j in range(max - l)])
    s += pad
    # print(letter,s)
    coded_len = "{:03b}".format(l)
    if gap:
        padding = zero_pad(6) + "1"
    else:
        padding = zero_pad(7)
    data = [s, padding, coded_len]
    binary = "".join(data)
    num = int(binary, base=2)
    if debug:
        print(letter, code, binary, num)
    return num


# decode test for checking
def expand(code):
    # print('{:016b}'.format(code))
    l = code & 7  # bottom 3 bits
    # print('{:016b}'.format(l))
    # print(l)
    bits = code >> 10
    print("{:06b}".format(bits), l)
    for i in range(l):
        print("!")


def decode(letter, d):
    n = ord(letter)
    if n in d:
        print(letter, d[n])
        expand(d[n])
    else:
        print("NO LETTER")


def decode_str(s, d):
    for i in s:
        decode(i, d)


def layout(d):
    # memory layout
    # duplicate into lower case
    empty = 0 | 16
    k = list(d.keys())
    for i in k:
        c = chr(i)
        if c.isupper():
            lc = c.lower()
            # add lower case
            d[ord(lc)] = d[i]
    for i in range(128):
        if i not in d:
            d[i] = empty
        if debug:
            print(i, chr(i), as_bits(d[i]))
    return d


def covert_to_init(d):
    data = []
    for i in range(128):
        data.append(d[i])
    return data


def build_mem(coding):
    alpha = convert(coding)
    layout(alpha)
    mem = covert_to_init(alpha)
    return alpha, mem


# elaboratable morse encoder
class Morse(Elaboratable):
    def __init__(self, mapping):
        self.enc = Memory(width=16, depth=128, init=mapping)
        self.read = self.enc.read_port()
        # incoming char
        self.input = stream.StreamSink(Layout([("data", 8)]))
        # output bitstream
        self.output = stream.StreamSource(Layout([("bitstrem", 1)]))

    def elaborate(self, platform):
        m = Module()
        # bind the memory
        m.submodules.mem = self.read

        # input
        char = Signal(7)  # 7 bit char

        # internals
        bits = Signal(6)
        length = Signal(3)
        space = Signal()
        nop = Signal()
        current = Signal(16)

        # bind the internals
        m.d.comb += [
            bits.eq(current[10:16]),
            length.eq(current[0:3]),
            space.eq(current[3]),
            nop.eq(current[4]),
            self.read.addr.eq(char),
            current.eq(self.read.data),
        ]

        # fsm variables
        bit_count = Signal(3)
        finished = Signal(reset=1)
        shreg = Signal(6)
        bit = Signal()

        # current bit is the head of the shift register
        m.d.comb += [bit.eq(shreg[-1])]

        # symbol counter
        symbol_count = Signal(6)
        symbol_incr = Signal(6)

        # gap counter

        gap_count = Signal(6)
        gap_incr = Signal(6)

        # letter gap counter

        letter_gap_count = Signal(6)
        letter_gap_incr = Signal(6)

        # output signals
        out_bit = Signal()
        out_data = Signal()
        out_valid = Signal()


        # debug
        letter_gap = Signal()

        with m.FSM() as fsm:
            # wait for somthing to happed
            with m.State("IDLE"):
                m.d.comb += self.input.ready.eq(1)
                with m.If(self.input.valid == 1):
                    m.d.comb += (self.input.ready.eq(0),)
                    m.d.sync += [
                        char.eq(self.input.data),  # 8 to 7 bits
                        finished.eq(0),
                    ]
                    m.d.sync += char.eq(self.input.data)
                    m.next = "RWAIT"

            # delay for memory read
            with m.State("RWAIT"):
                m.next = "START"

            # load the bit data , switch on nop
            with m.State("START"):
                m.d.sync += [bit_count.eq(length), shreg.eq(bits)]
                with m.If(nop == 1):
                    m.next = "IDLE"
                with m.Else():
                    m.next = "CHAR"

            # run through encoding for a character
            with m.State("CHAR"):
                m.d.sync += [
                    shreg.eq(shreg << 1),
                    bit_count.eq(bit_count - 1),
                    symbol_incr.eq(0),
                    gap_incr.eq(0),
                    out_data.eq(0),
                ]
                # SPACE
                with m.If(space == 1):
                    m.d.sync += [symbol_count.eq(morse_const.word_gap), out_bit.eq(0)]
                    m.next = "SYMBOL"
                with m.Else():
                    # DIT
                    with m.If(bit == 0):
                        m.d.sync += [
                            symbol_count.eq(morse_const.dit_length),
                            out_bit.eq(1),
                        ]
                        m.next = "SYMBOL"
                    # DAH
                    with m.If(bit == 1):
                        m.d.sync += [
                            symbol_count.eq(morse_const.dah_length),
                            out_bit.eq(1),
                        ]
                        m.next = "SYMBOL"
                with m.If(bit_count == 0):
                    m.d.sync += [
                        letter_gap_count.eq(morse_const.letter_gap),
                        letter_gap_incr.eq(0)
                    ]
                    m.next = "LETTER_GAP"

            # spool out the symbol
            with m.State("SYMBOL"):
                with m.If(symbol_incr == symbol_count):
                    m.d.sync += [
                        gap_count.eq(morse_const.symbol_gap),
                    ]
                    m.next = "GAP"
                with m.Else():
                    m.d.sync += [out_data.eq(out_bit)]
                    m.next = "SYMBOL_NEXT"

            with m.State("SYMBOL_NEXT"):
                m.d.comb += out_valid.eq(1)
                m.d.sync += symbol_incr.eq(symbol_incr + 1)
                m.next = "SYMBOL"

            # spool out the gap
            with m.State("GAP"):
                with m.If(gap_incr == gap_count):
                    m.next = "CHAR"
                with m.Else():
                    m.d.sync += [out_data.eq(0)]
                    m.next = "GAP_NEXT"

            with m.State("GAP_NEXT"):
                m.d.comb += out_valid.eq(1)
                m.d.sync += gap_incr.eq(gap_incr + 1)
                m.next = "GAP"

            # spool out the letter gap
            with m.State("LETTER_GAP"):
                with m.If(letter_gap_incr == letter_gap_count):
                    m.next = "IDLE"
                with m.Else():
                    m.d.sync += [out_data.eq(0)]
                    m.next = "LETTER_GAP_NEXT"

            with m.State("LETTER_GAP_NEXT"):
                m.d.comb += out_valid.eq(1)
                m.d.sync += letter_gap_incr.eq(letter_gap_incr + 1)
                m.next = "LETTER_GAP"
        return m


def sim_data(s, dut):
    def b(val):
        print(val, ord(val))
        yield dut.data.eq(ord(val))
        yield dut.valid.eq(1)
        yield
        yield dut.valid.eq(0)
        while (yield dut.ready) == 0:
            yield

    for i in s:
        yield from b(i)


if __name__ == "__main__":
    alpha, mem = build_mem(coding)
    # test_string = " sphinx of black quartz judge my vow "
    test_string = "MORSE CODE"
    # decode_str(test,alpha)

    mo = Morse(mem)
    if debug:
        print(alpha)
        print(mem)
    with pysim.Simulator(
        mo,
        vcd_file=open("morse.vcd", "w"),
        # gtkw_file=open("trig.gtkw", "w"),
        # traces=[tb.o, tb.counter],
    ) as sim:
        sim.add_clock(10)
        sim.add_sync_process(sim_data(test_string, mo.input))
        sim.run_until(5000, run_passive=True)
