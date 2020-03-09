# SLIP protocol 
# https://en.wikipedia.org/wiki/Serial_Line_Internet_Protocol

__working__ = False

from nmigen import * 
from nmigen.hdl.rec import Layout
import stream 

# Strean if chars 
char_stream = Layout([('char',8)])
# Slip Stream, layout is the same
slip_stream = Layout([('char',8)])

class SLIP_C:
    # some SLIP constants
    frame_end = 0xC0
    frame_escape = 0xDB
    transpose_frame_end = 0xDC
    transpose_frame_escape = 0xDD


class SLIP_Encode(Elaboratable):
    " encode a char stream into slip"
    def __init__(self):
        self.sink = stream.StreamSink(char_stream)
        self.source = stream.StreamSource(slip_stream)

    def elaborate(self,platform):
        m = Module()

        return m

class SLIP_Decode(Elaboratable):
    " decode a slip stream into char"
    def __init__(self):
        self.sink = stream.StreamSink(slip_stream)
        self.source = stream.StreamSource(char_stream)

    def elaborate(self,platform):
        m = Module()

        return m

class SLIP(Elaboratable):
    def __init__(self):
        self.encode = SLIP_Encode()
        self.decode = SLIP_Decode()

    def elaborate(self,platform):
        m = Module()
        m.submodules.encode = self.encode
        m.submodules.decode = self.decode

        return m

if __name__ == "__main__":
    print("SLIP SIMULATION")
    sl = SLIP()
    print(sl)

