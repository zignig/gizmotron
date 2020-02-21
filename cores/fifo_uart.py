# fifo wrapped uart

from nmigen import * 
from nmigen.lib.fifo import SyncFIFO

from .uart import RX,TX
from .gizmo import Gizmo, IO

class _FIFOUart(Elaboratable):
    def __init__(self,rx,tx,clk_freq,baud_rate,depth=128):
        # create the components
        self.TX = TX(tx, clk_freq, baud_rate)
        self.RX = RX(rx, clk_freq, baud_rate)
        self.RX_FIFO = SyncFIFO(width=8, depth=depth) 
        self.TX_FIFO = SyncFIFO(width=8, depth=depth) 
        
        #expose the interface
        self.rx_depth = self.RX_FIFO.level
        self.rx_data = self.RX_FIFO.r_data

        self.tx_depth = self.TX_FIFO.level
        self.tx_data = self.TX_FIFO.w_data

    def elaborate(self, platform):
        m = Module()

        # add the UART
        m.submodules.tx = self.TX
        m.submodules.rx = self.RX
        
        # add the FIFOs
        m.submodules.tx_fifo = self.TX_FIFO
        m.submodules.rx_fifo = self.RX_FIFO

        # bind them together
        # RX
        m.d.comb += [
            self.RX.ack.eq(self.RX_FIFO.w_rdy),
            self.RX_FIFO.w_en.eq(self.RX.rx_ready),
            self.fifo.w_data.eq(self.RX.rx_data),
        ]
        # TX
        print("BIND TX PLS") 
        return m
    
class FIFOUart(Gizmo):
    def build(self, **kwargs):
        serial = self.platform.request("uart", self.number)
        clock = self.platform.lookup(self.platform.default_clk).clock

        u = _FIFOUart(serial.rx,serial.tx,clock.frequency,self.baud,depth=self.depth)
        self.add_device(u)
        tx_data  = IO(sig_out=u.tx_data,sig_in=u.tx_depth,name="tx")
        self.add_reg(tx_data)

        rx_depth = IO(sig_in=u.rx_depth,name="rx_depth")
        self.add_reg(rx_depth)

        rx_data = IO(sig_in=u.rx_data,name="rx_data")
        self.add_reg(rx_data)

