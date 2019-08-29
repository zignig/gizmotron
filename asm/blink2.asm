MOVR R0,1
loop:
    ROTI R0,R0,1
    STXA R0,blinky
J loop

