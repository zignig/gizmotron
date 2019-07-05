#!/usr/bin/python3
from boneless.simulator import *
from boneless.arch.instr import *
from boneless.assembler.asm import Assembler
from boneless.arch.disasm import disassemble

import tty,sys
import termios
import atexit

end = False
exit = False
debug = True 
char = ''

from construct import CPU
from plat import BB
# silence warings 
from nmigen import *

Elaboratable._Elaboratable__silence = True

bcpu = CPU(BB())

def char_dev():
    global end 
    char = ord(sys.stdin.read(1))
    if char == 3: # control C
        end = True
        print("BREAK")
        return None
    return char

def io(addr, data=None):
    global exit,char,end,debug
    #print(addr,data)
    if data == None:
        if addr == 3: # rx status 
            char = char_dev()
            if char is not None:
                return 1
                print(char)
            else:
                return 0
        if addr == 4: # rx data
            #print("READ_CHAR "+chr(char))
            #print("RC")
            return char
        return 0
    else:
        if addr == 0: # userleds 
            return 
            print("LEDS_"+"{:016b}".format(data))
        if addr == 1:
            return 0 
        if addr == 2:
            #sys.stdout.write(u"\u001b[1000D")
            print("{:c}".format(data),end="",flush=True)

header = bcpu.b.asm_header()
cpu = BonelessSimulator(start_pc=0, mem_size=1024)
if len(sys.argv) > 1:
    file_name = sys.argv[1]
else:
    file_name = "asm/bootloader.asm"
asmblr = Assembler(debug=False, file_name=file_name)
asmblr.load_fragment(header)
asmblr.assemble()
asmblr.display()

cpu.load_program(asmblr.code)
cpu.register_io(io)

def line(asmblr):
    pc = str(cpu.pc).ljust(10)
    code = disassemble(cpu.mem[cpu.pc]).ljust(20)
    reg = cpu.regs()[0:8].tolist()
    stack = cpu.mem[9:15].tolist()
    if cpu.mem[cpu.pc] in asmblr.rev_labels:
        ref = asmblr.rev_labels[cpu.mem[cpu.pc]]
    else:
        ref = ""
    if cpu.pc in asmblr.rev_labels:
        label = asmblr.rev_labels[cpu.pc]
    else:
        label = ""
    print(pc, "|", code, "|", reg, "|" , stack,"->", label,"|",ref,"\r")

fd = sys.stdin.fileno()
oldtty_settings = termios.tcgetattr(fd)
tty.setraw(sys.stdin)

deadline = 500000
counter = 0
while not end:
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

termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty_settings)

