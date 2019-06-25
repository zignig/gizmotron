J init
; Some delay macros 

init:
    MOVI R0,2
    MOVI R4,49
    MOVI R5,60
loop:
    STX R4, R0, 0 
    CMP R4,R5
    JE init
    ADDI R4,1
    J loop

