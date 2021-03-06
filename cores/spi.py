from nmigen import * 
from periph.base import Peripheral,Register

@Register(driver="spi")
class SPI(Peripheral,Elaboratable):
    def __init__(self):
        super().__init__()
        bank = self.csr_bank()
        
        self._en      = bank.csr(1,'w')
        self._data_in = bank.csr(8,'w')
        self._data_out = bank.csr(8,'r')

    def elaborate(self,platform):
        m = Module()
        m.submodules._bridge = self._bridge
        return m
