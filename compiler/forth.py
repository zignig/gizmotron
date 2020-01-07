# a forth for boneless ,
# transcribed from itsy forth

from registers import *
from boneless.arch.opcode import *
from boneless.arch.asm import Assembler
import pprint

# running global reference.

last_ref = "init"


def glob(name, value, length=1):
    r = [L(name)]
    for i in range(length):
        r.append(value)
    return r


def header(name, imm=False):
    global last_ref
    r = [L(name)]
    assert len(name) < 32
    r.append(len(name))
    for i in name:
        r.append(ord(i))
    r.append(AR(last_ref))
    last_ref = name
    return r


def primitive(name, code):
    r = header(name)
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
            primitive("export", [ADDI(R0, R0, 2)])
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
