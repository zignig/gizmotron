# morse encoder

from nmigen import *
from nmigen.cli import pysim

# coding is 16 bits
# XXXXXX.....ngyyy
# X : dots and dashes
# . : undefined ( as yet )
# n : no encoding
# g : word gap
# y : length of code
import math

debug = False 

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
    word_gap = 7


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
        print(min_c,max_c)
        print(max_c-min_c)
    if debug:
        print("MAX ", max, power_of_2(max))
    d = {}
    for i, j in coding.items():
        num = encode(i, j, max)
        d[ord(i)] = num
    return d 

def as_bits(i):
    return '{:016b}'.format(i)


     
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
    data = [s, padding , coded_len]
    binary = "".join(data)
    num = int(binary, base=2)
    if debug:
        print(letter, code, binary, num)
    return num

# decode test for checking 
def expand(code):
    #print('{:016b}'.format(code))
    l = code & 7 # bottom 3 bits
    #print('{:016b}'.format(l))
    #print(l)
    bits = code >> 10 
    print('{:06b}'.format(bits),l)
    for i in range(l):
        print('!')

def decode(letter,d):
    n = ord(letter)
    if n  in d:
        print(letter,d[n])
        expand(d[n])
    else:
        print("NO LETTER")

def decode_str(s,d):
    for i in s:
        decode(i,d)

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
            print(i,chr(i),as_bits(d[i]))
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
    return alpha,mem

# elaboratable morse encoder
class Morse(Elaboratable):
    def __init__(self,mapping):
        self.enc = Memory(width=16,depth=128,init=mapping)
        self.current = Signal(16) # current signal to process
        self.read = self.enc.read_port()

    def elaborate(self,platform):
        m = Module()
        # bind the memory
        m.submodules.mem = self.read

        # internals
        data = Signal(6)
        length = Signal(3)
        space = Signal()
        nop = Signal()
        
        # temp counter 
        counter = Signal(8)
        next_c = Signal(8)
        m.d.sync += [
            counter.eq(counter+1),
            next_c.eq(counter),
        ]
        m.d.comb += [
            self.read.addr.eq(counter),
            self.current.eq(self.read.data),
        ]

        # bind the internals 
        m.d.comb += [
            data.eq(self.current[10:16]),
            length.eq(self.current[0:3]),
            space.eq(self.current[3]),
            nop.eq(self.current[4]),
        ]

        with m.FSM() as fsm:
            with m.State("IDLE"):
                pass        
        return m



if __name__ == "__main__":
    alpha , mem = build_mem(coding)
    test = "SOS"
    decode_str(test,alpha)

    mo = Morse(mem)
    if debug:
        print(alpha)
        print(mem)
    else:
        with pysim.Simulator(
            mo,
            vcd_file=open("morse.vcd", "w"),
            # gtkw_file=open("trig.gtkw", "w"),
            #traces=[tb.o, tb.counter],
        ) as sim:
            sim.add_clock(1)
            #sim.add_sync_process(runner())
            sim.run_until(5000, run_passive=True)
