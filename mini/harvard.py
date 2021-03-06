from nmigen import *
from core import CPU, MetaInstr, Instr, PC
from mem import RAM


class DataMem(Instr):
    """
        Data memory
    """

    data = RAM()

    def devices(self):
        return self.data


class Harvard(CPU):
    class data(Instr):
        r = DataMem()

        def device(self):
            return self.r

        def fetch(self):
            pass

    class inc(data):
        def execute(self):
            self.r.eq(self.r + 1)

    class J(PC):
        pass


h = Harvard()
h.show()
