# Periphs auto attach to a the boneless IO
from nmigen import *
from collections import OrderedDict
from nmigen_soc.csr.bus import Multiplexer,Element,Decoder

__all__ = ["PeriphCollection","Periph","IO"]
# This is a reqork of gizmo to use
# the CSR system in nmigen-soc

class EpicFail(BaseException):
    pass


class PeriphCollection:
    " A collection of periphs "
    debug = True
    def __init__(self,addr_width=16,data_width=16):
        self.mplex = Multiplexer(addr_width=addr_width,data_width=data_width)

        self._modules = [] 
        self._prepared = False
        self._name_map  = OrderedDict()
        self._name_count = OrderedDict()

    def __next__(self):
        print('next')

    def __iadd__(self, mod):
        if type(mod) == type([]):
            for m in mod:
                self._modules.append(m)
        else:
            self._modules.append(mod)
        return self

    def dump(self):
        for i in self._modules:
            print(i)

    def addr_map(self):
        " return an address map to (periph,register) tuple"
        m = {} 
        for i in self.mplex.bus.memory_map.all_resources():
            print('>',i[0].name,i)
            name = i[0].name
            l = i[1][1] -  i[1][0]
            start = i[1][0]
            print('len :',l)
            if l == 1:
               m[name] = start
            else:
               for j in range(l):
                    m[name+"_"+str(j)] = start+j
        return m

    def attach(self,m):
        " attach all the periphs to csr bus"
        if not self._prepared:
            self.prepare()
        for i,j in self._name_map.items():
            if self.debug:
                print(i,j)
            j.attach(m,self.mplex)

    def prepare(self):
        "Normalize names and multi bind"
        if self._prepared == False:
            print("not prepared")
            for i in self._modules:
                self._name_map[i.name] = i
            self._prepared = True
 
        for i,j in self._name_map.items():
            j.prepare(self.mplex)

    def asm_header(self):
        txt = '; automatic periph headers\n'
        m = self.addr_map()
        for i,j in m.items(): 
            reg_name = i 
            reg_id = j
            txt += '.equ '+reg_name+','+str(reg_id)+'\n'
        return txt


# TODO create asm definitions named correctly
class BIT:
    " create a named bit register"

    def __init__(self, name, pos):
        self.name = name
        self.pos = pos

    def dump(self, name):
        print("\t" + name + "_" + self.name + " -> " + str(self.pos))


class IO:
    """ 
    Define and bind a read write register
    maps ext_port inside a boneless processor 
    """

    def __init__(self, sig_in=None, sig_out=None, name=None):
        self.sig_in = sig_in
        self.sig_out = sig_out
        self.bits = []
        self._assigned = False
        if name is not None:
            self.name = name
        self.width = 0 
        # calc max width
        if self.has_input():
            if self.sig_in.shape().width > self.width:
                self.width = self.sig_in.shape().width
        if self.has_output():
            if self.sig_out.shape().width > self.width:
                self.width = self.sig_out.shape().width

    def set_addr(self, addr):
        self.addr = addr

    def add_bit(self, bit):
        self.bits.append(bit)

    def has_input(self):
        if self.sig_in is not None:
            return True
        else:
            return False

    def has_output(self):
        if self.sig_out is not None:
            return True
        else:
            return False

    def __repr__(self):
        return "\n\t"+ self.name+ "\n\t\tin  : " + str(self.sig_in) + "\n\t\tout : " + str(self.sig_out) + "\n\twidth :" + str(self.width)


class Periph:
    " A periph is a wrapper around an Elaboratable module that binds to the external interface of the Boneless-CPU"
    debug = True 

    def __init__(self, name, platform=None, **kwargs):
        for i, j in kwargs.items():
            setattr(self, i, j)
        self.platform = platform
        self.name = name
        self.registers = [] # a list of IO 
        self.elements = [] # a list of CSR elements
        self.devices = [] # a list of Elboratables to add
        self.code = ""  # assembly code for the periph TODO , auto attach
        self._prepared = False
        self.build()

    def dump(self):
        data = []
        for r in self.registers:
            tmp = r.dump()
            data.append(tmp)
        return data

    def build(self):
        " add the modules and IO and BITS to itself"
        raise EpicFail(self)

    def simulator(self):
        " TODO , create interfaces for the simulator"
        raise EpicFail(self)

    def add_device(self, dev):
        " add a Module to the periph "
        self.devices.append(dev)

    def add_reg(self, reg):
        " add an Autobinding register to the Boneless CPU"
        self.registers.append(reg)

    def prepare(self,mplex):
        if len(self.registers) > 0:
            for reg in self.registers:
                if not reg._assigned:
                    reg._assigned = True
                    if self.name not in self.__dir__():
                        setattr(self,reg.name,reg)
                    # Create the Element
                    acc = 'r'
                    if reg.has_output():
                        acc = 'w'
                    if reg.has_input():
                        acc = 'r'
                    if reg.has_input() and reg.has_output():
                        acc = 'rw'
                    el = Element(width=reg.width,name=reg.name,access=acc)
                    self.elements.append(el)
                    # add register info to the element
                    el.sig_out = reg.sig_out
                    el.sig_in = reg.sig_in
                    mplex.add(el)

    def attach(self,m,mplex):
        " Generate and bind the gateware to the Boneless "
        if not self._prepared:
            self.prepare(mplex)
        if self.debug:
            print("<< " + self.name + " >>")
        if len(self.elements) > 0:
            for el in self.elements:
                if el.access.readable():
                    if self.debug:
                        print("Binding Input ")
                        print(el.sig_in)
                    with m.If(el.r_stb):
                        m.d.sync += el.r_data.eq(el.sig_in)
                if el.access.writable():
                    if self.debug:
                        print("Binding Output ")
                        print(el.sig_out)
                    with m.If(el.w_stb):
                        m.d.sync += el.sig_out.eq(el.w_data)
        if len(self.devices) > 0:
            for dev in self.devices:
                m.submodules += dev

    def __repr__(self):
        return (
            self.name + str(self.devices) + "|" + str(self.registers)
        )


class TestPeriph(Periph):
    "Test Periph"
    code = "NOP"

    def build(self):
        r = IO(Signal(), Signal(50), name="first")
        r.add_bit(BIT("bit_a", 0))
        r.add_bit(BIT("bit_b", 1))
        self.add_reg(r)
        r = IO(Signal(), Signal(3), name="second")
        self.add_reg(r)

class Other(Periph):
    def build(self):
        for i in range(10):     
            r = IO(Signal(), Signal(50), name="num"+str(i))
            self.add_reg(r)
            
# Fake classes for testing
class ex_int:
    def __init__(self):
        self.addr = Signal(16)
        self.r_en = Signal()
        self.w_en = Signal()
        self.r_data = Signal(16)
        self.w_data = Signal(16)


class FakeBoneless:
    def __init__(self):
        self.ext_port = ex_int()
        self.addr = 0


if __name__ == "__main__":
    d = Decoder(addr_width=16,data_width=16)
    a = PeriphCollection(d)
    print("Activate the Periphtron")
    a += [
        TestPeriph("test"),
        TestPeriph("fnord"),
        #Other('hello'),
        ]
    m = Module()
    print("attach")
    a.attach(m)
    print("finish attach")
