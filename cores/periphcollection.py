from nmigen import * 
from nmigen_soc.csr import Decoder 
from nmigen_soc.csr.bus import Multiplexer, Element, Decoder
from periph.base import Peripheral, PeripheralBridge

Elaboratable._Elaboratable__silence = True

class Map:
    def __init__(self):
        self._dict = {} 

    def _add(self,name,value):
        if name not in self._dict:
            setattr(self,name,value)
            self._dict[name] = value

    def _show(self):
        for i,j in self._dict.items():
            print(i,j)
    

class PeripheralCollection(Elaboratable):
    def __init__(self,addr_width=16,data_width=16):
        self._decoder = Decoder(addr_width=addr_width,data_width=data_width)

        self.data_width = data_width
        self.mem = self._decoder.bus.memory_map
        self.devices = []
        self.map = Map()

        self._built = False
        

    def add(self,item):
        print(item)
        self.devices.append(item)

    def build(self):
        if not self._built:
            # bind and add the bus if the device does not have one 
            for i in self.devices:
                try:
                    self._decoder.add(i.bus)
                    print(dir(i))
                except NotImplementedError as e:
                    print(e)
                    i._bridge = i.bridge(data_width=self.data_width) 
                    i.bus = i._bridge.bus
                    self._decoder.add(i.bus)
            # map all the CSR devices
            for i,(start,end,width) in self.mem.all_resources():
                length = end - start
                print(i,start,end,width,i.access,length)
                #if i.access.readable() and i.access.writeable():
                if length  > 1:
                    for j in range(length):
                        self.map._add(i.name+"_"+str(j),start+j)
                else:
                   self.map._add(i.name,start)
            self._built = True

    def show(self):
        self.build()
        return self.map
        
    def elaborate(self, platform):
        self.build()
        m = Module()
        m.submodules.bus = self._decoder
        for i in self.devices:
            m.submodules[i.name] = i 
        return m        
