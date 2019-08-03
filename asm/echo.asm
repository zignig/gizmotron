.window
J init
.alloc leds,1
.alloc pad,32
.equ delay,1
; Basic echo construct
; Need macros and register renames

checkrx:
    LDXA R3,rx_status
    CMPI R1,1
    JE addtopad
    JR R7,0  ; no change in status , jump back to main loop
addtopad:
    LDXA R2,rx_data
    MOVI R3,1
    STXA R3,rx_status
    STXA R2,blinky
JR R7,0

txchar:
    STXA R2,tx_data
    MOVI R3,1
    STXA R3,tx_status
    MOVI R3,0
    STXA R3,tx_status
waitup:
    LDXA R3,tx_status
    CMPI R3,1
    JE waitup
waitdown:
    LDXA R3,tx_status
    CMPI R3,0
    JE waitdown
JR R7,0

init:
    MOVI R0,0 ; working register 
    MOVI R1,0 ; working address 
    MOVI R2,32; holding data 
    MOVI R3,0 ; device status
    MOVI R4,0 ; delayer
    MOVI R5,0 ; 
    MOVI R6,0 ; 
    MOVI R7,0 ; jump return address

run:
    JAL R7,txchar

    CMPI R2,126 ; loop through readable chars
    JE resetChar
    ADDI R2,R2,1
    J run
resetChar:
    MOVI R2,32
J run


    
