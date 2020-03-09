# SLIP protocol 
# https://en.wikipedia.org/wiki/Serial_Line_Internet_Protocol

__working__ == False

from nmigen import * 
from nmigen.hdl.rec import Layout
import stream 

char_stream = Layout([('char',8)])

class SLIP(Elaboratable):

    # some SLIP constants
    frame_end = 0xC0
    frame_escape = 0xDB
    transpose_frame_end = 0xDC
    transpose_frame_escape = 0xDD

    def __init__(self):
        self.sink = stream.StreamSink(char_stream)
        self.source = stream.StreamSource(char_stream)

    def elaborate(self,platform):
        m = Module()

        return m


if __name__ == "__main__":
    print("SLIP SIMULATION")
    sl = SLIP()
    print(sl)

