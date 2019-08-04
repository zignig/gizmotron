.window
J init
.alloc leds,1
.alloc pad_count,1
.alloc pad,32
.equ delay,1
; Basic echo construct
; Need macros and register renames

checkrx:                        ; get a char off the serial port 
    LDXA R3,rx_status           ; load the RX status from the serial port
    CMPI R3,1                   ; compare the register to 1
    JE addtopad                 ; if it is equal to one ,  add it to the pad
    JR R7,0                     ; no change in status , jump back to main loop
addtopad:
    LDXA R2,rx_data             ; load the RX data from the serial port
    MOVI R3,1                   ; load 1 into to R3
    STXA R3,rx_status           ; acknowledge the char in the serial port
    MOVI R3,0                   ; load 0 into to R3
    STXA R3,rx_status           ; acknowledge the char in the serial port
    STXA R2,blinky              ; write to blinky
JR R7,0

txchar:                         ; put a char into the serial port 
    STXA R2,tx_data             ; put the holding data into the serial port
    MOVI R3,1                   ; set status to one
    STXA R3,tx_status           ; write to tx status 
    MOVI R3,0                   ; set the status to zerop
    STXA R3,tx_status           ; acknowledge the wrtie 
waitup:                         ; TODO , this should be a fifo in the serial port 
    LDXA R3,tx_status           ; wait for tx status to go high
    CMPI R3,1
    JE waitup
waitdown:
    LDXA R3,tx_status           ; wait for the status to go low
    CMPI R3,0
    JE waitdown
JR R7,0

init:                           ; initialize the program all the registers.
    MOVI R0,0 ; working register        
    MOVI R1,0 ; working address 
    MOVI R2,32; holding data 
    MOVI R3,0 ; device status
    MOVI R4,0 ; delayer
    MOVI R5,0 ; 
    MOVI R6,0 ; 
    MOVI R7,0 ; jump return address

run:                                   ; main loop
    ;JAL R7,txchar                      ; write r2 ( holding ) to the serial port 
    JAL R7,checkrx                      ; get a char from the serial port
    CMPI R2,126                         ; loop through readable chars
    JE resetChar                        ; this is TX testing 
    ADDI R2,R2,1
    J run
resetChar:
    MOVI R2,32
J run


    
