# attempt at a register allocator
from collections import OrderedDict
import random

__all__ = ["LocalLabels", "SubR", "Window", "MetaSub", "Firmware"]

"""
ideas

allocate variables into a register bank, break it into windows 
limit the total number of windows and spill into ram if needed

work out how to make sure that the variables are in the correct window
for actions 

minimise the amount of spill an copying from one window to the other

? contiguous windows
? linked list of windows
? dynamic window allocation

multi register allocations ? 
pointer deferencing ? 

###

from conversations with tpwrules and looking at his programming style.
The use of a frame stack where each subroutine call moves the register window 
up 8 register.

- Loads the needed registers from the preceeding frame
- Allocates local variables 
- Runs the subroutine code
- And then return jumps from the parent frame.
- The parent routine can then pluck register values out of the child frame.

This is quite elegant. A subroutine becomes.

assuming R6 is the Frame pointer (fp)

If you need to pass variables up and down

    LD(var1,fp,1) # load the first register of the prevuis frame into var1 
    LD(var2,fp,2) # second register
    LDW(fp,-8) # put the previous window address into R6

    # other code
    # blah blah blah


    Then return up
    ADJW(8) # move the window to the previous frame address
    JR(R7,0) # the return jump is in the parent frame

    ST(return_val,fp,-3) # put the value it register 3 in the frame above

If nothing needs to be passed up or down

    ADJW(8)
    # blah blah blah 
    ADJW(-8)
    JR(R7,0)

and you don't lose a register for the frame pointer.

When you want to call a subroutine , it's just

    JAL(R7,'subroutine')

and tada, it runs and makes the registers available to the above frame.

Kind of nifty.

rehack of https://github.com/tpwrules/ice_panel/blob/master/bonetools.py

"""

from boneless.arch.opcode import *


class RegError(Exception):
    pass


class NameCollision(RegError):
    pass


class WindowFull(RegError):
    pass


class BadParamCount(RegError):
    pass


class LocalLabels:
    """ Local random labels for inside subr
        create a local labeler
        ll = LocalLabels()
        make a label - ll('test')
        reference the label - ll.test
    """

    def __init__(self):
        self._postfix = "_{}".format(random.randrange(2 ** 32))
        self._names = {}

    def __call__(self, name):
        self._names[name] = self._postfix + name
        setattr(self,name,name  +  self._postfix )
        return L(name + self._postfix )

    def __getattr__(self, key):
        if key in self._names:
            return self._names[key]
        # for forward declarations
        self._names[key] = key + self._postfix
        setattr(self,key,key + self._postfix )
        return self._names[key]


class Window:
    _REGS = [R0, R1, R2, R3, R4, R5, R6, R7]
    _size = 8

    def __init__(self, jumper=True):
        self._allocated = [False] * 8
        self._name = [""] * 8
        if jumper:
            # frame for subroutine calls R6 is fp , R7 is return
            self._allocated[6] = True
            self._name[6] = "fp"
            setattr(self, "fp", self._REGS[6])

            self._allocated[7] = True
            self._name[7] = "ret"
            setattr(self, "ret", self._REGS[7])

    def req(self, name):
        if type(name) == type(""):
            self._single(name)
        if type(name) == type([]):
            for i in name:
                self._single(i)

    def _single(self, name):
        for i in range(self._size):
            if self._allocated[i] == False:
                # free register
                self._allocated[i] = True
                self._name[i] = name
                if name not in self.__dict__:
                    setattr(self, name, self._REGS[i])
                    return
                else:
                    raise NameCollision(self)
        # no free registers
        # fail for now
        raise WindowFull(self)

    def __getitem__(self, key):
        if hasattr(self, key):
            return self.__dict__[key]

    # TODO spill and reuse registers

class VectorTable:

    _size = 8

    def __init__(self,name="no_name"):
        self.labels = OrderedDict()
        self.name = name

    def __getattr__(self,key):
        if key in self.labels:
            print('get ',key)
            return self.lables[key]

    def __setattr__(self,key,value):
        self.__dict__[key] = value
        if key not in ['labels','name']:
            print('set ',key,' to ',value)
            self.labels[key] = value

    def dump(self):
        for i in self.labels.items():
            print(i)

class MetaSub(type):
    subroutines = []
    """
    Meta Sub is a class for collecting all the routines together
    It also expands the useds subroutines for adding in the epilogue of the
    program
    """

    def __new__(cls, clsname, bases, attrs):
        newclass = super(MetaSub, cls).__new__(cls, clsname, bases, attrs)
        cls.register(newclass)  # here is your register function
        return newclass

    def register(cls):
        d = MetaSub.subroutines
        if cls.__qualname__ == "SubR":
            # Don't add root subclass
            return
        if cls not in d:
            d.append(cls())

    @classmethod
    def code(cls):
        li = MetaSub.subroutines
        # loop through and add sub-subroutines to the list
        c = []
        while True:
            old_c = c
            c = []
            for i in li:
                if i._called:
                    c.append(i.code())
            if len(old_c) == len(c):
                break
        return c


class SubR(metaclass=MetaSub):
    """
    Calling Standard
    R7 = return address (used by the child frame)
    R6 = frame pointer

    
    """

    _called = False

    def __init__(self):
        self.w = Window()
        self.setup()
        if not hasattr(self, "name"):
            self.name = type(self).__qualname__
        if hasattr(self, "params"):
            self.length = len(self.params)
            for i in self.params:
                self.w.req(i)
        else:
            self.length = 0
        if hasattr(self, "locals"):
            for i in self.locals:
                self.w.req(i)

    @classmethod
    def mark(cls):
        " include code if the subroutine has been called "
        cls._called = True

    def setup(self):
        pass

    def __call__(self, *args):
        if len(args) != self.length:
            raise ValueError("Parameter count is should be '{}'".format(self.length))
        # load the parameters into the next frame
        instr = []
        for i, j in enumerate(args):
            source = j
            target = self.w[self.params[i]].value
            instr += [LD(source, self.w.fp, -8 + target)]
        instr += [JAL(self.w.ret, self.name)]
        self.mark()
        return instr

    def instr(self):
        " empty code "
        return []

    def code(self):
        prelude = [L(self.name)]
        data = []
        data += [LDW(self.w.fp, -8)]  # window shift up
        data += self.instr()
        data += [ADJW(8), JR(R7, 0)]
        prelude += [data]
        return prelude


class Firmware:
    def __init__(self, start_window=0x1000):
        self.w = Window()
        self.sw = start_window

    def instr(self):
        return []

    def code(self):
        fw = [
            L("init"),
            MOVI(w.fp, self.sw),
            STW(w.fp),
            L("main"),
            self.instr(),
            J("main"),
            L("ExtraCode"),
            MetaSub.code(),
        ]
        return fw


# Test Objects


class Printer(SubR):
    def setup(self):
        self.params = ["addr", "data"]

    def instr(self):
        w = self.w
        return [STX(w.addr, w.data, 0)]


class Degenerate(SubR):
    pass


class Reboot(SubR):
    def setup(self):
        self.w.req("counter")
        self.w.req("switch")

    def instr(self):
        ll = LocalLabels()
        w = self.w
        return [ANDI(R0, R0, 0), ll("test"), ADDI(w.counter, w.switch, 1), JZ(ll.test)]


class Composite(SubR):
    def setup(self):
        self.params = ["addr"]
        self.w.req("counter")
        self.w.req("delay")
        self.r = Reboot()
        self.p = Printer()

    def instr(self):
        ll = LocalLabels()
        w = self.w
        return [self.r(), self.p(self.w.addr, self.w.counter)]


class Outer:
    reboot = Reboot()
    printer = Printer()
    comp = Composite()


w = Window()
w.req("addr")
w.req("counter")
w.req("data")
