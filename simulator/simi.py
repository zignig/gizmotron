
class SimInstr(object):
    def __init__(self,instr,sim):
        self.instr = instr
        self.sim = sim

    def call(self):
        if self.sim.has_exti:
            print("Extended instruction")
            self.sim.has_exti = False
            val = self.sim.exti_val << 3
            print(val)
            self.instr.imm.value  = val + self.instr.imm.value
            #TODO fix this
        else:
            self.run()

    def __repr__(self):
        return self.instr.__repr__()
    
    # short name access
    @property
    def rsd(self):
        return self.instr.rsd.value

    @property
    def imm(self):
        return self.instr.imm.value

    @property
    def ra(self):
        return self.instr.ra.value 

    def set_reg(self,reg,val):
        self.sim.set_reg(reg,val)

    def reg(self,reg):
        return self.sim.get_reg(reg)

    # simulator function
    @property
    def pc(self):
        return self.sim.pc

