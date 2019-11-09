# attempt at a register allocator
from collections import OrderedDict


class Register:
    def __init__(self, name="blank", temp=-1, size=1):
        self.name = name
        self._allocated = False
        self.temperature = temp
        self.size = size  # for multiword variables

    def __repr__(self):
        txt = str(self.name) + " ["
        if self._allocated:
            txt += "X"
        else:
            txt += " "
        txt += "] (" + str(self.temperature) + ")"
        return txt


class Holding:
    # Holds all the variables in the program
    def __init__(self):
        self.count = 0
        self.reg = OrderedDict()

    def insert(self, target):
        r = Register(target)


class Window:
    def __init__(self, size=8):
        self.size = size
        self.reg = [Register(None) for reg in range(self.size)]

    def spill(self):
        print("SPILL")

    class Action:
        def __init__(self, reg, source, target):
            self.reg = reg
            self.source = source
            self.target = target

        def __repr__(self):
            return (
                str(type(self).__qualname__)
                + " : "
                + str(self.source)
                + "--"
                + str(self.target)
            )

    class Spill(Action):
        pass

    class Use(Action):
        pass

    class LoadFrom(Action):
        pass

    def request(self, target):
        # ask for a specific var
        for pos, reg in enumerate(self.reg):
            if target == reg:
                reg.temperature += 1
                return self.Use(pos, reg, None)
        # not available load
        for pos, reg in enumerate(self.reg):
            if reg._allocated == False:
                self.reg[pos] = target
                target._allocated = True
                return self.LoadFrom(pos, target, reg)
        # uh oh, no emptys
        # spill the lowest temperature register
        temperature = 1e6
        ret_reg = None
        ret_pos = 0
        for pos, reg in enumerate(self.reg):
            if reg.temperature < temperature:
                temperature = reg.temperature
                ret_reg = reg
                ret_pos = pos
        self.reg[ret_pos] = target
        target.temperature += 1
        target._allocated = True
        return self.Spill(ret_pos, target, ret_reg)


w = Window()
a = Register("one")
b = Register("two")
c = Register("three")
d = Register("four")
e = Register("five")
f = Register("six")
g = Register("seven")
h = Register("eight")
r = [a, b, c, d, e, f, g, h]
# for i in r:
#    w.request(i)
