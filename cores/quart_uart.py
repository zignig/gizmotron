from nmigen import *
from nmigen.lib.cdc import MultiReg
from nmigen.lib.fifo import SyncFIFO
from nmigen.tools import bits_for


__all__ = ["AsyncSerialRX", "AsyncSerialTX", "AsyncSerial"]


def _wire_layout(data_bits):
    return [("start", 1), ("data", data_bits), ("stop", 1)]


class AsyncSerialRX(Elaboratable):
    def __init__(self, *, divisor, divisor_bits=None, data_bits=8, pins=None, depth=0):
        self.divisor = Signal(divisor_bits or bits_for(divisor), reset=divisor)

        self.data = Signal(data_bits)
        self.err = Record([("overflow", 1), ("frame", 1)])
        self.rdy = Signal()
        self.ack = Signal()

        self.i = Signal()

        self._pins = pins
        self.depth = depth

    def elaborate(self, platform):
        m = Module()

        timer = Signal.like(self.divisor)
        shreg = Record(_wire_layout(len(self.data)))
        bitno = Signal(max=len(shreg))

        if self.depth > 0:
            self._fifo = SyncFifo(len(self.data), self.depth)
            m.d.submodules += self._fifo

        if self._pins is not None:
            m.d.submodules += MultiReg(self._pins.rx.i, self.i, reset=1)

        with m.FSM():
            with m.State("IDLE"):
                with m.If(~self.i):
                    m.d.sync += [bitno.eq(len(shreg) - 1), timer.eq(self.divisor >> 1)]
                    m.next = "BUSY"

            with m.State("BUSY"):
                with m.If(timer != 0):
                    m.d.sync += timer.eq(timer - 1)
                with m.Else():
                    m.d.sync += [
                        shreg.eq(Cat(self.i, shreg)),
                        bitno.eq(bitno - 1),
                        timer.eq(self.divisor),
                    ]
                    with m.If(bitno == 0):
                        m.next = "DONE"

            with m.State("DONE"):
                with m.If(self.ack):
                    m.d.sync += [
                        self.data.eq(shreg.data),
                        self.err.frame.eq(~((shreg.start == 0) & (shreg.stop == ~0))),
                    ]
                m.d.sync += self.err.overflow.eq(~self.ack)

        with m.If(fsm.ongoing("DONE")):
            m.d.sync += self.rdy.eq(1)
        with m.Elif(self.ack):
            m.d.sync += self.rdy.eq(0)

        return m


class AsyncSerialTX(Elaboratable):
    def __init__(self, *, divisor, divisor_bits=None, data_bits=8, pins=None):
        self.divisor = Signal(divisor_bits or bits_for(divisor), reset=divisor)

        self.data = Signal(data_bits)
        self.rdy = Signal()
        self.ack = Signal()

        self.o = Signal()

        self._pins = pins

    def elaborate(self, platform):
        m = Module()

        timer = Signal.like(self.divisor)
        shreg = Record(_wire_layout(len(data)))
        bitno = Signal(max=len(shreg))

        if self._pins is not None:
            m.d.comb += self._pins.tx.o.eq(self.o)

        with m.FSM():
            with m.State("IDLE"):
                m.d.comb += self.rdy.eq(1)
                m.d.sync += self.o.eq(shreg[0])
                with m.If(self.ack):
                    m.d.sync += [
                        shreg.start.eq(0),
                        shreg.data.eq(self.data),
                        shreg.stop.eq(~0),
                        bitno.eq(len(shreg) - 1),
                        timer.eq(self.divisor),
                    ]
                    m.next = "BUSY"

            with m.State("BUSY"):
                with m.If(timer != 0):
                    m.d.sync += timer.eq(timer - 1)
                with m.Else():
                    m.d.sync += [
                        Cat(self.o, shreg).eq(shreg),
                        bitno.eq(bitno - 1),
                        timer.eq(self.divisor),
                    ]
                    with m.If(bitno == 0):
                        m.next = "IDLE"

        return m


class AsyncSerial(Elaboratable):
    def __init__(self, *, divisor, divisor_bits=None, **kwargs):
        self.divisor = Signal(divisor_bits or bits_for(divisor), reset=divisor)

        self.rx = AsyncSerialRX(**kwargs)
        self.tx = AsyncSerialTX(**kwargs)

    def elaborate(self, platform):
        m = Module()
        m.submodules.rx = self.rx
        m.submodules.tx = self.tx
        m.d.comb += [self.rx.divisor.eq(self.divisor), self.tx.divisor.eq(self.divisor)]
        return m
