from boneless.arch.asm import Assembler

a = Assembler()
a.parse_text(open('blink.asm').read())
d = a.assemble()
print(d)
e = a.disassemble(d)
print(e)
