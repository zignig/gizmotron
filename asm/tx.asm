J init
; Some delay macros 

init:
    MOVI R0,2
    MOVI R1,1
    MOVI R4,49
    MOVI R5,60
loop:
    STX R4, R0, 0 
    STX R1, R1, 0
wait:
    LDX R6, R1,0
    CMP R3,R6
    JE wait

    CMP R4,R5
    JE init

    ADDI R4,1
    STX R3, R1, 0
    J loop

