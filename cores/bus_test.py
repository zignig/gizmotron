from nmigen import * 
from nmigen_soc.csr import Decoder 
from periph.serial import AsyncSerialPeripheral
from periph.timer import TimerPeripheral 
from periph.bork import BorkPeripheral 
from nmigen_soc import wishbone

class reg:
    def __init__(self):
        self._dict = {} 

    def add(self,name,value):
        if name not in self._dict:
            setattr(self,name,value)
            self._dict[name] = value

    def show(self):
        for i,j in self._dict.items():
            print(i,j)
    

class BusTest(Elaboratable):
    def __init__(self,uart_divisor,uart_pins):
        self._arbiter = wishbone.Arbiter(addr_width=16, data_width=16,
                                         features={"cti", "bte"})
        self._decoder = wishbone.Decoder(addr_width=16, data_width=16,
                                         features={"cti", "bte"})
        
        self.uart = AsyncSerialPeripheral(divisor=uart_divisor, pins=uart_pins)
        self._decoder.add(self.uart.bus)

        self.uart2 = AsyncSerialPeripheral(divisor=uart_divisor, pins=uart_pins)
        self._decoder.add(self.uart2.bus)

        self.timer = TimerPeripheral(32)
        self._decoder.add(self.timer.bus)

        self.timer2 = TimerPeripheral(32)
        self._decoder.add(self.timer2.bus)

        self.bork = BorkPeripheral(32)
        self._decoder.add(self.bork.bus)

        self.mem = self._decoder.bus.memory_map

    def show(self):
        l = []
        r = reg()
        for i,(start,end,width) in self.mem.all_resources():
            print(i,start,end,width)
            length = end - start
            if length  > 1:
                for j in range(length):
                    r.add(i.name+"_"+str(j),start+j)

            else:
               r.add(i.name,start)
            l.append(i)
        return r,l
        
    def elaborate(self, platform):
        m = Module()

        m.submodules.uart    = self.uart

        m.d.comb += [
            self._arbiter.bus.connect(self._decoder.bus),
        ]

        return m        
if __name__ == "__main__":
    bt = BusTest(uart_divisor=9000,uart_pins="")
    r,l = bt.show()
    
