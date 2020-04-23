from nmigen import * 
from periph.base import Peripheral,Register

@Register(driver="spi")
class SPI(Peripheral,Elaboratable):
    __driver__ = "spi"
    def __init__(self):
        super().__init__()
        bank = self.csr_bank()
        
        self.data_in = bank.csr(8,'w')
        self.data_out = bank.csr(8,'w')

    def elaborate(self,platform):
        m = Module()
        m.submodules._bridge = self._bridge
        return m
