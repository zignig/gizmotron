from boneless.arch.opcode import * 
from boneless.arch.asm import *
from boneless.arch.instr import Instr

def bounce(code):
    print(code)
    asmb = Assembler()
    asmb.parse(code)
    print("Assembler Input")
    print(asmb.input)
    a = asmb.assemble()
    print("Coded Input")
    print(a)
    d = asmb.disassemble(a,as_text=True)
    #d = asmb.disassemble(a)
    print("Disassembled Code")
    print(d)
    print("Info")
    print(asmb.info())

if __name__ == "__main__":
    print("Boneless Test")
    code = [
        L('hello'),
        MOVI(R0,4),
        MOVI(R1,3),
        ADD(R0,R1,R2),
        AR('hello'),
        RR('hello'),
        NOP(0),
        RR('hello'),
        RR('test'),
        NOP(0),
        NOP(0),
        NOT(R0,R4),
        L('test'),
    ]
    code_a = """
                ADD  R1, R1, R0
                ORI  R2, R3, 123
            loop:
                J    loop
                .word 5678
            """
    code_b = [
        ADDI(R0,R0,'foo'),
    ]
    code_c = """
\tSUB\tR2, R1, R4\t\t; 1234
\tST\tR6, R3, 0x918\t\t; C123 5678
\tEXTI\t0x123\t\t\t; C123
\tXOR\tR0, R5, R0\t\t; 00B0
\tBZ0\t-0x1\t\t\t; B0FF
\t.word\t0xffff
    """
    bounce(code)
    #bounce(code_a)
    #bounce(code_b) 
    #bounce(code_c)
