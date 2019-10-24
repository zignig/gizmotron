from nmigen import * 
from nmigen_soc.csr.bus import * 

class Counter(Elaboratable):
    def __init__(self,width=16):
        self.en = Signal()
        self.counter = Signal(width)

    def elaborate(self,platform):
        m = Module()
        with m.If(self.en == 1):
            m.d.sync += self.counter.eq(self.counter +1)
        return m


class csrCounter(Elaboratable):
    def __init__(self,width=16,csr=None):
        self.width = width
        self.csr =  csr
        print("CSR COUNTER")

    def elaborate(self,platform):
        m = Module()
        m.submodules.counter = counter = Counter(self.width)
        en = CSRElement(width=1)
        val  = CSRElement(width=self.width)
        with m.If(en.w_stb):
            m.d.comb +=  counter.en.eq(en.r_data)
        with m.If(val.r_stb):
            m.d.comb += val.r_data.eq(counter.counter)
        self.csr.add(en)
        self.csr.add(val)

