from nmigen import *
from nmigen.utils import bits_for


class stack(Elaboratable):
    def __init__(self, width=16, depth=32):
        self.rdat = Signal(width)
        self.wdat = Signal(width)
        self.we = Signal()
        self.re = Signal()
        self.pos = Signal(bits_for(depth))  # counter
        self.updown = Signal()
        self.depth = depth

        self.mem = Memory(width=width, depth=depth)

    def elaborate(self, platform):
        m = Module()
        m.submodules.rdport = rdport = self.mem.read_port()
        m.submodules.wrport = wrport = self.mem.write_port()

        with m.If(self.updown):
            m.d.comb += self.pos.eq(self.pos + 1)
        with m.Else():
            m.d.comb += self.pos.eq(self.pos - 1)

        m.d.comb += [
            rdport.addr.eq(self.pos),
            self.rdat.eq(rdport.data),
            wrport.addr.eq(self.pos),
            wrport.data.eq(self.wdat),
            wrport.en.eq(self.we),
        ]
        return m


if __name__ == "__main__":
    import argparse
    from nmigen import cli

    parser = argparse.ArgumentParser()
    cli.main_parser(parser)
    args = parser.parse_args()

    tb = stack()
    ios = (tb.pos, tb.rdat)

    cli.main_runner(parser, args, tb, name="stack", ports=ios)
