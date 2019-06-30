import opcode_mod_v3

# fragments
class frag: val=0
class opcode: bits=5
class op5: bits=5
class op4: bits=4
class op3: bits=3
class register: bits=3
class t: bits=2
class imm3: bits=3
class imm5: bits=5
class imm8: bits=8
class F: bits=1
class cond: bits=3
class off8: bits=8
class imm13: bits=13


# instructions
class inst:
    bits=16

class RRR(inst): layout = [opcode,register,register,t,register] 
class RR3(inst): layout = [opcode,register,register,t,imm3]
class RR5(inst): layout = [opcode,register,register,imm5]
class R8(inst): layout = [opcode,register,imm8] 
class C(inst): layout = [op4,F,cond,off8]
class E(inst): layout = [op3,imm13] 
class X(inst): layout = [op3,imm13]

# instruction splits 
sp = {
        5:[RRR],
        4:[RRR,RR3],
        3:[C,E,X]
}

# generate the instructions set
def generate():
    groups = []
    li = dir(opcode_mod_v3)
    for i in li:
        # all operations
        if i.startswith('OPCODE'):
            sp = i.split("_")
            sec = int(sp[0].lstrip('OPCODE'))
            if sec == 5:
            print(sec)
            groups.append(sp)

    for i in groups:
        print(i)

generate()
