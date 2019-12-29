from nmigen import *

from mem import RAM
from stack import Stack


class ProgramCounter(Elaboratable):
    def __init__(self, reset):
        self.i_addr = Signal(16)
        self.r_addr = Signal(16, reset=reset)

        self.c_set = Signal()
        self.c_inc = Signal()

    def elaborate(self, platform):
        m = Module()

        with m.If(self.c_set):
            m.d.sync += self.r_addr.eq(self.i_addr)
        with m.Elif(self.c_inc):
            m.d.sync += self.r_addr.eq(self.r_addr + 1)

        return m


class MetaInstr(type):

    class tree:
        def __init__(self, cls):
            self.name = cls
            self.children = []

        def add(self, c):
            self.children.append(c)

        def walk(self):
            if len(self.children) > 0:
                for i in self.children:
                    print(i)
                    i.walk()

        def insert(self, cls):
            li = cls.mro()
            li.reverse()
            li = li[1:]
            for i in li:
                print(i)
            print("--")

    def __new__(cls, clsname, bases, attrs):
        newclass = super(MetaInstr, cls).__new__(cls, clsname, bases, attrs)
        cls.register(newclass)  # here is your register function
        return newclass

    def register(cls):
        if not hasattr(cls,"_registry"):
            setattr(cls,"_registry",set())
        if not hasattr(cls,"_heirachy"):
            setattr(cls,"_heirachy",MetaInstr.tree(object))

        if cls.__qualname__ == "Instr":
            # Don't add root subclass
            return
        cls._registry.add(cls)
        cls._heirachy.insert(cls)

    def ShowTree(cls):
        for i in cls._registry:
            l = i.mro()
            l.reverse()
            l = l[1:]
            print(l)


class Instr(metaclass=MetaInstr):
    def __init__(self):
        pass


class PC(Instr):
    pc = ProgramCounter(reset=0)

    def device(self):
        return self.pc

    def execute(self, m):
        m.d.sync += self.pc.c_inc.eq(True)


class Ram(Instr):
    r = RAM()

    def device(self):
        return self.r

    def fetch(self):
        pass


class CPU(Instr):
    states = ["fetch", "decode", "execute"]

    def registers(self, count):
        for i in range(count):
            type("R" + str(i), (self.reg,), {})

    def __init__(self, width=64):
        self.devices = set()

    def show(self):
        for i in self._registry:
            instr = i()
            if hasattr(instr, "device"):
                print(instr)
                self.devices.add(instr.device())
        print("Devices")
        for i in self.devices:
            print("\t", i)

        for i in self.states:
            print("", i)
            for j in self._registry:
                inst = j()
                if hasattr(inst, i):
                    print("\t", inst)

    def elaborate(self, platform):
        m = Module()

        with m.FSM():
            for i in self.states:
                with m.State(i):
                    pass
        return m
