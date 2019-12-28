from nmigen import * 


class ProgramCounter(Elaboratable):
    def __init__(self, reset):
        self.i_addr = Signal(16)
        self.r_addr = Signal(16, reset=reset)

        self.c_set  = Signal()
        self.c_inc  = Signal()

    def elaborate(self, platform):
        m = Module()

        with m.If(self.c_set):
            m.d.sync += self.r_addr.eq(self.i_addr)
        with m.Elif(self.c_inc):
            m.d.sync += self.r_addr.eq(self.r_addr + 1)

        return m


class MetaInstr(type):
    instructions = []
    class tree:
        def __init__(self,cls):
            self.name = cls 
            self.children = []

        def add(self,c):
            self.children.append(c)
        
        def walk(self):
            if len(self.children)> 0:
                for i in self.children:
                    print(i)
                    i.walk()
 
        def insert(self,cls):
            li = cls.mro()
            li.reverse()
            li = li[1:]
            for i in li:
                print(i)
            print('--')
            
    heirachy = tree(object)

    def __new__(cls, clsname, bases, attrs):
        newclass = super(MetaInstr, cls).__new__(cls, clsname, bases, attrs)
        cls.register(newclass)  # here is your register function
        return newclass

    def register(cls):
        d = MetaInstr.instructions
        if cls.__qualname__ == "Instr":
            # Don't add root subclass
            return
        if cls not in d:
            d.append(cls)
        MetaInstr.heirachy.insert(cls)

    @classmethod
    def tree(cls):
        for i in MetaInstr.instructions:
            l = i.mro()
            l.reverse()
            l = l[1:]
            print(l)

class Instr(metaclass=MetaInstr):
    def __init__(self):
        pass


class PC(Instr):
    pc = ProgramCounter(0)
    def device(self):
        return self.pc  

class JUMP(PC):
    def decode(self,m):
        return m
        
        
class Test(Instr):
    def fetch(self):
        pass

    def execute(self):
        pass


class Test2(Instr):
    def decode(self):
        pass


class Test3(Test2):
    def execute(self):
        pass


class ALU(Instr):
    pass

class ADD(ALU):
    pass

class SUB(ALU):
    pass

class REG(Instr):
    pass

class jump(Instr):
    pass

def registers(count):
    for i in range(count):
        type('R'+str(i),(REG,),{})

class CPU(Elaboratable):
    def __init__(self):
        self.instr = MetaInstr.instructions
        self.states = ['fetch','decode','execute']
        registers(16)

    def show(self):
        for i in self.instr:
            instr = i()
            if hasattr(instr,'device'):
                print(instr.device())

        for i in self.states:
            print(i)
            for j in self.instr:
                inst = j()
                if hasattr(inst,i):
                    print(inst," has ",i) 
                
    def elaborate(self,platform):
        m = Module()
        
        with m.FSM():
            for i in self.states:
                with m.State(i):
                    pass
        return m


c = CPU()
c.show()
MetaInstr.tree()

