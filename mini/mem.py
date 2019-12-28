from nmigen import * 

# memory / io bus 


def Device():
    pass

class RAM(Elaboratable):
    def __init__(self,width=16,depth=32):
        self.addr = Signal(width)
        self.rdat = Signal(width)
        self.wdat = Signal(width)
        self.we = Signal()
        self.re = Signal()
        self.depth = depth

        self.mem = Memory(width=width,depth=depth,init=self.start())

    def start(self):
        data = [] 
        return data 

    def elaborate(self,platform):
        m = Module()
        m.submodules.rdport = rdport = self.mem.read_port()
        m.submodules.wrport = wrport = self.mem.write_port()
        m.d.comb += [
            rdport.addr.eq(self.addr),
            self.rdat.eq(rdport.data),
            wrport.addr.eq(self.addr),
            wrport.data.eq(self.wdat),
            wrport.en.eq(self.we),
        ]
        return m

class IO(Elaboratable):
    def __init__(self,width=16):
        self.addr = Signal(width)
        self.rdat = Signal(width)
        self.wdat = Signal(width)
        self.we = Signal()
        self.re = Signal()

    def elaborate(self,platform):
        m = Module()
        return m 
        
