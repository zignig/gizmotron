from registers import *
from boneless.arch.opcode import *
from boneless.arch.asm import Assembler
import pprint


class Stringer(Block):
    class WriteString(SubR):
        def setup(self):
            self.params = ["address"]
            self.locals = ["length","finish","char"]

        def instr(self):
            w = self.w
            ll = LocalLabels()
            return [
                LD(w.length,w.address,0),
                CMPI(w.length,0),
                Rem('empty string continue'),
                BEQ(ll.exitdump),
                Rem("calculate the end of the string"),
                ADD(w.finish,w.address,w.length),
                ll("nextchar"),
                ADDI(w.address,w.address,1),
                LD(w.char,w.address,0),
                Rem("TODO call tx out"),
                CMP(w.address,w.finish),
                BLTU(ll.nextchar),
                ll("exitdump"),
            ]
    writestring = WriteString()

"""
dumpstring:
    LD R0,R1,0                  ; load the length of the string into R0 
    CMPI R0,0                   ; empty string , go back
    BEQ exitdump
    AND R5,R1,R1                ; copy address into temp
    ADD R5,R5,R0                ; add the length to the address
    ; R1 is the current address
    ; R5 is the end of the string
nextchar:
    ADDI R1,R1,1                ; increment the pointer
    LD   R2,R1,0                ; load the data at working address into holding
    JAL  R7,txchar              ; write the char
    CMP  R1,R5                  ; compare current with end of string
    BLTU nextchar               ; not there yet, get next char
exitdump:
    JR R6,0                     ; return with jump2
"""
