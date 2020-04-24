from nmigen import * 
from periph.base import Peripheral,Register

class Testing(Peripheral,Elaboratable):
    def __init__(self):
        super().__init__()
        bank = self.csr_bank()
        

        for i in range(50):
            c = bank.csr(1,'rw',name="reg_"+str(i))
            
    def elaborate(self,platform):
        m = Module()
        m.submodules._bridge = self._bridge
        return m
