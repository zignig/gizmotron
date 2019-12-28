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
        r = RAM()

        def device(self):
            return self.r

        def fetch(self):
            pass

    class J(PC):
        pass


h = Harvard()
h.show()
