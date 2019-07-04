import opcode_mod_v3 as opc
import types,sys

# fragments
class frag: 
    def __init__(self,val):
        self.val = val

class opcode(frag): bits=5
class op5(frag): bits=5
class op4(frag): bits=4
class op3(frag): bits=3
class t(frag): bits=2
class F(frag): bits=1
class cond(frag): bits=3

# mutable fragments
class mut(frag):
    pass

class imm3(mut): bits=3
class imm5(mut): bits=5
class imm8(mut): bits=8
class off8(mut): bits=8
class imm13(mut): bits=13

class register(mut): 
    bits=3
    def __init__(self):
        pass

class rsd(register): pass
class ra(register): pass
class rb(register): pass

# instructions
class inst:
    bits=16

class RRR(inst): layout = [opcode,rsd,ra,t,rb] 
class RR3(inst): layout = [opcode,rsd,ra,t,imm3]
class RR5(inst): layout = [opcode,rsd,ra,imm5]
class R8(inst): layout = [opcode,rsd,imm8] 
class C(inst): layout = [op4,F,cond,off8]
class E(inst): layout = [op3,imm13] 
class X(inst): layout = [op3,imm13]

# bind the new class into the global namespace 
def bind(cls):
    ns = sys._getframe(1).f_globals
    ns[cls.name] = cls
    print(cls)
    
# build commands based on split
def full(data):
    print('full - ',data)
    #cls = type(spl,(RRR,),{'name':spl})
    #bind(cls)

def modal(data):
    print('modal',data)
    com = data[2][data[0]]
    opcd = getattr(opc,data[1]) 
    # absolute
    for i in com:
        cls = type(i,(RRR,),{'name':i,'opcode':opcode(opcd)})
        bind(cls)
    # imm
    for i in com:
        cls = type(i+"I",(RR3,),{'name':i+'I','t':'hello'})
        bind(cls)

def extended(data):
    print('extended',data)

splits = {
    5: full,
    4: modal,
    3: extended
}

# generate the instructions set
def generate():
    sub = {} 
    li = dir(opc)
    # split up the types
    for i in li:
        print(i)
        if i.startswith('OPTYPE'):
            sp = i.lstrip('OPTYPE2_').split('_')
            if sp[0] not in sub:
                sub[sp[0]] = [sp[1]]
            else:
                sub[sp[0]].append(sp[1])
    for i in li:
        # all operations
        if i.startswith('OPCODE'):
            sp = i.split("_")
            sec = int(sp[0].lstrip('OPCODE'))
            # based on the code
            splits[sec]((sp[1],i,sub))

generate()
