# attempt at a register allocator
from collections import OrderedDict

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

from conversations with tpw_rules and looking at his programming style.
The use of a frame stack where each subroutine call moves the register window 
up 8 register.

- Loads the needed registers from the preceeding frame
- Allocates local variables 
- Runs the subroutine code
- Copies return variable down 
- Shifts the window back down 
- And then return jumps from the parent frame.

This is quite elegant. A subroutine becomes.

assuming R6 is the Frame pointer (fp)

If you need to pass variables up and down

    LDW(fp,-8) # put the previous window address into R6
    LD(var1,fp,1) # load the first register of the prevuis frame into var1 
    LD(var2,fp,2) # second register

    # other code
    # blah blah blah

    ST(return_val,fp,3) # put the value it register 3 in the frame above

    Then return up
    ADJW(8) # move the window to the previous frame address
    JR(R7,0) # the return jump is in the parent frame

If nothing needs to be passed up or down

    ADJW(8)
    # blah blah blah 
    ADJW(-8)
    JR(R7,0)

and you don't lose a register for the frame pointer.

When you want to call a subroutine , it's just

    JAL(R7,'subroutine')

and tada, it runs and puts variables back into the current frame.

Kind of nifty.

"""


class Register:
    def __init__(self, name="blank", temp=-1, size=1):
        self.ref = None
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
