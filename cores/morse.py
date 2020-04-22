# morse encoder
# Simon Kirkby 20200309
# obeygiantrobot@gmail.com

__working__ = True 

from nmigen import *
from nmigen.cli import pysim
from nmigen.back.pysim import Tick
from nmigen.hdl.rec import Layout
import stream, math

debug = False  # True

# Util Functions
def power_of_2(x):
    return 1 if x == 0 else math.ceil(math.log2(x))


def as_bits(i):
    return "{:016b}".format(i)


def zero_pad(l):
    pad = "".join(["0" for j in range(l)])
    return pad


# Primary Coding Map
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
    letter_gap = 2  # actually 3 has a symbol gap
    word_gap = 1  # actually 7 has a letter gap


# encode the morse into binary


def convert(coding):
    " take a key:value dictionary and convert it "
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


# coding is 16 bits
# XXXXXX.....ngyyy
# X : dots and dashes
# . : undefined ( as yet )
# n : no encoding
# g : word gap
# y : length of code


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


def layout(d):
    " Fill out the lookup table "
    # memory layout
    empty = 0 | 16  # only has the NOP bit set
    k = list(d.keys())
    # duplicate into lower case
    for i in k:
        c = chr(i)
        if c.isupper():
            lc = c.lower()
            # add lower case
            d[ord(lc)] = d[i]
    # everything else is a NOP
    for i in range(128):
        if i not in d:
            d[i] = empty
        if debug:
            print(i, chr(i), as_bits(d[i]))
    return d


def covert_to_init(d):
    " remove keys and return a init map for Memory"
    data = []
    for i in range(128):
        data.append(d[i])
    return data


def build_mem(coding):
    " Build the map and a memory block"
    alpha = convert(coding)
    layout(alpha)
    mem = covert_to_init(alpha)
    return alpha, mem


# define layouts
char_incoming = Layout([("data", 8)])
bitstream = Layout([("bitstream", 1)])

# elaboratable morse encoder
class Morse(Elaboratable):
    " takes a byte stream and converts it to a morse bitstream "

    def __init__(self, mapping):
        # memory for the lookup table
        self.enc = Memory(width=16, depth=128, init=mapping)
        self.read = self.enc.read_port()
        # incoming char
        self.sink = stream.StreamSink(char_incoming)
        # output bitstream
        self.source = stream.StreamSource(bitstream)

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
        ready = Signal()
        shreg = Signal(6)
        bit = Signal()

        # output signals
        out_bit = Signal()
        out_data = Signal()
        out_valid = Signal()

        # streaming interface
        # input
        # m.d.comb += self.sink.ready.eq(self.source.ready & ready)
        m.d.comb += self.sink.ready.eq(ready)
        # output
        m.d.comb += [self.source.valid.eq(out_valid), self.source.data.eq(out_data)]

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

        # Main FSM for processing
        with m.FSM() as fsm:
            # wait for somthing to happen
            with m.State("IDLE"):
                m.d.comb += ready.eq(1)
                with m.If(self.sink.valid & ready):
                    m.d.sync += [char.eq(self.sink.data)]  # 8 to 7 bits
                    m.d.sync += char.eq(self.sink.data)
                    m.next = "RWAIT"

            # delay for memory read
            with m.State("RWAIT"):
                m.d.comb += ready.eq(0)
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
                # End of the char , add the gap
                with m.If(bit_count == 0):
                    m.d.sync += [
                        letter_gap_count.eq(morse_const.letter_gap),
                        letter_gap_incr.eq(0),
                    ]
                    m.next = "LETTER_GAP"

            # spool out the symbol
            with m.State("SYMBOL"):
                with m.If(symbol_incr == symbol_count):
                    m.d.sync += [gap_count.eq(morse_const.symbol_gap)]
                    m.next = "GAP"
                with m.Else():
                    m.d.comb += out_valid.eq(1)
                    m.d.sync += [out_data.eq(out_bit)]
                    m.next = "SYMBOL_NEXT"

            with m.State("SYMBOL_NEXT"):
                with m.If(self.source.ready):
                    m.d.comb += out_valid.eq(0)
                    m.d.sync += symbol_incr.eq(symbol_incr + 1)
                    m.next = "SYMBOL"

            # spool out the gap
            with m.State("GAP"):
                with m.If(gap_incr == gap_count):
                    m.next = "CHAR"
                with m.Else():
                    m.d.comb += out_valid.eq(1)
                    m.d.sync += [out_data.eq(0)]
                    m.next = "GAP_NEXT"

            with m.State("GAP_NEXT"):
                with m.If(self.source.ready):
                    m.d.comb += out_valid.eq(0)
                    m.d.sync += gap_incr.eq(gap_incr + 1)
                    m.next = "GAP"

            # spool out the letter gap
            with m.State("LETTER_GAP"):
                with m.If(letter_gap_incr == letter_gap_count):
                    m.next = "IDLE"
                with m.Else():
                    m.d.comb += out_valid.eq(1)
                    m.d.sync += [out_data.eq(0)]
                    m.next = "LETTER_GAP_NEXT"

            with m.State("LETTER_GAP_NEXT"):
                with m.If(self.source.ready):
                    m.d.comb += out_valid.eq(0)
                    m.d.sync += letter_gap_incr.eq(letter_gap_incr + 1)
                    m.next = "LETTER_GAP"

        return m


class BlinkOut(Elaboratable):
    """ 
    Takes a bitstream 
    bitstream = Layout([("bitstream",1)])
    and clock streches it by interval
    """

    def __init__(self, interval=20):
        self.sink = stream.StreamSink(bitstream)
        self.interval = interval
        self.out = Signal()

    def elaborate(self, platform):
        m = Module()

        # bit interval
        interval_counter = Signal(range(self.interval + 1))
        with m.If(interval_counter == self.interval):
            m.d.sync += interval_counter.eq(0)
            m.d.comb += self.sink.ready.eq(1)
        with m.Else():
            m.d.sync += interval_counter.eq(interval_counter + 1)
            m.d.comb += self.sink.ready.eq(0)

        with m.If(self.sink.valid & self.sink.ready):
            m.d.sync += self.out.eq(self.sink.data)

        return m


# Wrap the morse object with some FIFOs
class MorseWrap(Elaboratable):
    def __init__(self, mapping):
        self.input = stream.SyncFIFOStream(char_incoming,1)
        self.morse = Morse(mapping)
        self.blink = BlinkOut()

        self.output = stream.SyncFIFOStream(bitstream,1)

        # expose the streaming interfaces
        # TODO ask awygle if this is the best way
        self.sink = self.input.sink
        # self.sink = self.morse.sink
        self.source = self.output.source

    def elaborate(self, platform):
        m = Module()
        # add the submodules
        m.submodules.input = self.input
        m.submodules.output = self.output
        m.submodules.morse = self.morse
        m.submodules.blink = self.blink

        # bind the streams

        m.d.comb += [
            self.morse.sink.connect(self.input.source),
            self.output.sink.connect(self.morse.source),
            self.blink.sink.connect(self.output.source),
        ]

        return m


def sim_data(s, sink, source):
    def b(val):
        while not (yield sink.ready):
            yield
        print(val, ord(val))
        yield sink.data.eq(ord(val))
        yield sink.valid.eq(1)
        yield Tick()
        yield sink.valid.eq(0)
        yield Tick()

    for i in s:
        yield from b(i)


if __name__ == "__main__":
    alpha, mem = build_mem(coding)
    test_string = " sphinx of black quartz judge my vow "
    # test_string = " morse code "
    #test_string = "SOS SOS SOS"
    # test_string = "SOS"

    # mo = Morse(mem)
    mo = MorseWrap(mem)
    if debug:
        print(alpha)
        print(mem)
    with pysim.Simulator(mo, vcd_file=open("morse.vcd", "w")) as sim:
        sim.add_clock(10)
        sim.add_sync_process(sim_data(test_string, mo.sink, mo.source))
        sim.run_until(100000, run_passive=True)
