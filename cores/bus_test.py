from nmigen import * 
from nmigen_soc.csr import Decoder 
from periph.serial import AsyncSerialPeripheral
from periph.timer import TimerPeripheral 
from periph.bork import BorkPeripheral 
from nmigen_soc import wishbone

from nmigen_soc.csr.bus import Multiplexer, Element, Decoder
from plat import BB
from nmigen_boards.tinyfpga_bx import TinyFPGABXPlatform

class reg:
    def __init__(self):
        self._dict = {} 

    def _add(self,name,value):
        if name not in self._dict:
            setattr(self,name,value)
            self._dict[name] = value

    def _show(self):
        for i,j in self._dict.items():
            print(i,j)
    

class BusTest(Elaboratable):
    def __init__(self,uart_divisor,uart_pins):
        #self._arbiter = wishbone.Arbiter(addr_width=16, data_width=16, features={"cti", "bte"})
        #self._decoder = wishbone.Decoder(addr_width=16, data_width=16, features={"cti", "bte"})
        self._decoder = Decoder(addr_width=16,data_width=16)
        
        print(uart_pins)        
        self.uart = AsyncSerialPeripheral(divisor=uart_divisor, pins=uart_pins)
        self._decoder.add(self.uart.bus)

        #self.uart2 = AsyncSerialPeripheral(divisor=uart_divisor, pins=uart_pins)
        #self._decoder.add(self.uart2.bus)

        #self.timer = TimerPeripheral(32)
        #self._decoder.add(self.timer.bus)

        #self.timer2 = TimerPeripheral(32)
        #self._decoder.add(self.timer2.bus)

        self.bork = BorkPeripheral(32)
        self._decoder.add(self.bork.bus)

        self.mem = self._decoder.bus.memory_map

    def show(self):
        l = []
        r = reg()
        for i,(start,end,width) in self.mem.all_resources():
            print(i,start,end,width)
            length = end - start
            #print(i.access)
            if length  > 1:
                for j in range(length):
                    r._add(i.name+"_"+str(j),start+j)

            else:
               r._add(i.name,start)
            l.append(i)
        return r,l
        
    def elaborate(self, platform):
        m = Module()

        #m.submodules.uart    = self.uart
        m.submodules.bork = self.bork

        return m        

class t(Elaboratable):
    def elaborate(self,platform):
        m = Module()
        s = Signal(16)
        m.d.sync += s.eq(s + 1)
        return m


class myBus(Elaboratable):
    def __init__(self,bus):
        self.bus = bus

    def elaborate(self, platform):
        clk = platform.request(platform.default_clk, 0)
        print(clk)
        m = Module()
        m.domains.sync = ClockDomain()
        m.d.comb += ClockSignal().eq(clk.i)

        t1 = t()
        m.submodules.test = t1
        #m.submodules.bus = self.bus 
        return m

if __name__ == "__main__":
    
    platform = BB()
    u = platform.request('uart',0)
    uart_divisor = int(platform.default_clk_frequency // 9600 )
    bt = BusTest(uart_divisor=uart_divisor,uart_pins=u)

    r,l = bt.show()

    m = myBus(bt)

    platform.build(m) 
