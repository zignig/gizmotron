#!/usr/bin/python3
from boneless.simulator import *
from boneless.arch.instr import *
from boneless.assembler.asm import Assembler
from boneless.arch.disasm import disassemble

import tty,sys

end = False
exit = False
strin = ""
debug = False 
char = ''

from construct import CPU
from plat import BB

bcpu = CPU(BB())
print(bcpu.b)


def io(addr, data=None):
    global strin, exit
    if data == None:
        if addr == 10:
            return 0
        if addr == 1:
            return 0
        if addr == 3:
            char = ord(sys.stdin.read(1))
            return 1
        return 0
    else:
        if addr == 2:
            print(chr(data), end="")
        if addr == 1:
            print("")
            exit = True


header = bcpu.b.asm_header()
cpu = BonelessSimulator(start_pc=0, mem_size=1024)
if len(sys.argv) > 1:
    file_name = sys.argv[1]
else:
    file_name = "asm/echo.asm"
asmblr = Assembler(debug=False, file_name=file_name)
asmblr.load_fragment(header)
asmblr.assemble()
asmblr.display()
cpu.load_program(asmblr.code)
cpu.register_io(io)


def get_line():
    global strin, debug
    strin = input(">")
    if strin.startswith("\\"):
        if strin[1:] == "d":
            debug = not debug
        strin = ""


def line(asmblr):
    pc = str(cpu.pc).ljust(10)
    code = disassemble(cpu.mem[cpu.pc]).ljust(20)
    reg = cpu.regs()[0:8].tolist()
    stack = cpu.mem[9:15].tolist()
    rstack = cpu.mem[16:24].tolist()
    if cpu.mem[cpu.pc] in asmblr.rev_labels:
        ref = asmblr.rev_labels[cpu.mem[cpu.pc]]
    else:
        ref = ""
    if cpu.pc in asmblr.rev_labels:
        label = asmblr.rev_labels[cpu.pc]
    else:
        label = ""
    print(pc, "|", code, "|", reg, "|")  # , stack,"|",rstack, "->", label,"|",ref)


tty.setraw(sys.stdin)
deadline = 5000
counter = 0
while not end:
    while 1:
        cpu.stepi()
        if debug:
            line(asmblr)
        if exit:
            exit = False
            break
        counter += 1
        if counter == deadline:
            end = True
            break
    #get_line()
