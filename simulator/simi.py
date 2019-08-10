
class SimInstr(object):
    def __init__(self,instr,sim):
        self.instr = instr
        self.sim = sim
        self.exti_tmp = 0
        self.exti = False

    def call(self):
        if self.sim.has_exti:
            val = self.sim.exti_val << 3
            self.exti_tmp = val + self.instr.imm.value
            self.exti = True
            self.run()
            self.exti = False
            self.sim.has_exti = False
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
        if self.exti:
            return self.exti_tmp
        else:
            return self.instr.imm.value

    @property
    def ra(self):
        return self.instr.ra.value 

    @property
    def rb(self):
        return self.instr.rb.value

    # value of register a
    @property
    def rav(self):
        return self.reg(self.instr.ra.value)

    # value of reginster b
    @property
    def rbv(self):
        return self.reg(self.instr.rb.value)

    def set_reg(self,reg,val):
        self.sim.set_reg(reg,val)

    def reg(self,reg):
        return self.sim.get_reg(reg)

    # simulator function
    @property
    def pc(self):
        return self.sim.pc

