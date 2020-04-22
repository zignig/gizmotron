from nmigen import * 
from nmigen_soc.csr import Decoder 
from nmigen_soc.csr.bus import Multiplexer, Element, Decoder

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
    

class Peripheral(Elaboratable):
    def __init__(self):
        self._decoder = Decoder(addr_width=16,data_width=16)
        self.mem = self._decoder.bus.memory_map
        self.devices = []
        self._built = False

    def add(self,item):
        self.devices.append(item)

    def show(self):
        if not self._built:
            for i in self.devices:
                self._decoder.add(i.bus)
                print(i.name)
            self._built = True
        r = reg()
        for i,(start,end,width) in self.mem.all_resources():
            print(i,start,end,width,i.access)
            length = end - start
            if length  > 1:
                for j in range(length):
                    r._add(i.name+"_"+str(j),start+j)

            else:
               r._add(i.name,start)
        return r
        
    def elaborate(self, platform):
        m = Module()
        return m        
