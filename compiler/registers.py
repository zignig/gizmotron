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

rehack of https://github.com/tpwrules/ice_panel/blob/master/bonetools.py

"""

from boneless.arch.opcode import *

class RegError(Exception):
    pass 

class NameCollision(RegError):
    pass

class WindowFull(RegError):
    pass

class Register:
    def __init__(self,name,reg):
        self.name = name
        self.r = reg

    def __call__(self):
        return self.r
        
    
class Window:
    _REGS = [R0,R1,R2,R3,R4,R5,R6,R7]
    _size = 8
    def __init__(self):
        self._allocated = [False] * 8
        self._name = ['']*8

    def req(self,name):
        for i in range(self._size):
            if self._allocated[i] == False:
                # free register
                self._allocated[i] = True
                self._name[i] = name
                if name not in dir(self):
                    reg = Register(name,self._REGS[i])
                    setattr(self,name,reg())
                else:
                    raise NameCollision(self)
                return reg()
        # no free registers
        # fail for now
        raise WindowFull(self)
                    
    def __getattr__(self,name):
        return self.req(name)
        
        
class MetaCall(type):
    pass
       
class Call:
    def __init__(self,name,*vars):
        self.name = name 
        self.w = Window()
        self.inreg = vars
        print("--",name,"--")
        for i in enumerate(vars):
            print(i)

    def instr(self):
        print("OVERRIDE_ME")
        return []

    def loader(self):
        # grabs code from the register above
        loads = []
        for i in  self.inreg:
            print(i)
            loads.append(LD(self.w.test,self.w.fp,i.value))
        return loads
            
        
    def code(self):
        prelude = [L(self.name)]
        prelude += [LDW(self.w.fp,-8)] # window shift up
        prelude += self.loader()
        prelude += self.instr()
        prelude += [ADJW(8),JR(R7,0)] 
        return prelude

            

class FrameStack:
    def __init__(self):
        self.windows = [Window()]
        self.pointer = 0 # pointer to the currenet window

    def fetch(self,name):
        # search through the windows and find the name
        # produce LD(target_reg,frame_pointer,< offset >
        # this gets a bit hairy over multiple frames
        pass

    

w = Window()
w.test
w.fnord
w.gorf
