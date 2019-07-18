from boneless.arch.asm import Assembler
from boneless.arch import opcode ,mc , instr
a = Assembler()
a.parse_text(open('echo.asm').read())
print("---INPUT---")
print(a.input)
d = a.assemble()
print("---MACHINE CODE---")
print(d)
e = a.disassemble(d)
print("---DISASSEMBLE---")
print(e)
