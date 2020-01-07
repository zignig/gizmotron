# a forth for boneless ,
# transcribed from itsy forth

from registers import *
from boneless.arch.opcode import *
from boneless.arch.asm import Assembler
import pprint

# running global reference.

last_ref = "init"

class String:
    def __init__(self,name):
        assert len(name) < 32
        self.name = name

    def __repr__(self):
        return "String('"+self.name+"')"

    def __call__(self,sym):
        r = [len(self.name)]
        for i in self.name:
            r.append(ord(i))
        return r

        
def glob(name, value, length=1):
    r = [L(name)]
    for i in range(length):
        r.append(value)
    return r


def header(name, imm=False):
    global last_ref
    r = [AR(last_ref)]
    r.append(L(name))
    last_ref = name
    r.append(String(name))
    r.append(L("xt_"+name))
    return r


def primitive(name, code):
    r = header(name)
    r.append(code)
    return r

def variable(name):
    r = header(name)
    code = [
            J('init'),
            ]
    r.append(code)
    return r

def docol(name, code, imm=False):
    r = header(name, imm)
    r.append(code)
    return r


# some words

def comma():
    return [primitive("comma", [])]

class Forth(Firmware):

    def instr(self):
        w = self.w
        w.req("stackp")
        w.req("returnp")
        w.req("insp")
        w.req("xtp")
        w.req("tos")
        w.req("temp")
        return [
            header("test"),
            header("hello"),
            header("fnord"),
            primitive("export", [ADDI(R0, R0, 2)]),
            variable('tib')
            # docol('fnord',[L('wot')]),
            # glob('state',0),
            # glob('>in',0),
            # glob('#tib',0),
            # glob('base',10),
            # glob('dp',0),
            # glob('stack',0,32),
            # glob('rstack',0,32)
        ]


if __name__ == "__main__":
    bl = Forth()
    code = bl.code()
    pprint.pprint(code)
    asm = Assembler()
    asm.parse(code)
    bin = asm.assemble()
    print(bin)
