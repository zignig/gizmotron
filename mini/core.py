from nmigen import * 


class ProgramCounter(Elaboratable):
    def __init__(self, reset):
        self.i_addr = Signal(16)
        self.r_addr = Signal(16, reset=reset)

        self.c_set  = Signal()
        self.c_inc  = Signal()

    def elaborate(self, platform):
        m = Module()

        with m.If(self.c_set):
            m.d.sync += self.r_addr.eq(self.i_addr)
        with m.Elif(self.c_inc):
            m.d.sync += self.r_addr.eq(self.r_addr + 1)

        return m

