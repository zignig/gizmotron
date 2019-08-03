; Blinky testing
.equ data,R0
J loop

.macro delay    ; macro will inset this code inline
    MOVI R1,65535
    JAL R7,wait ; jump to wait
.endm

wait:
    SUBI R2,R2, 1 ; count down 
    CMP R2,R3  ; compare to zero , R3 is unused
    JNZ wait   ; if the are not equal , keep counting down
    JR R7,0    ; return to the address in R7

loop:
    STX R1,data, 0 ; Write R1 to the user leds
    ADDI R1,R1, 1    ; increment
    delay         ; Wait
    J loop        ; Again
