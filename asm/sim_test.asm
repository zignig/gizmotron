; automatic gizmo headers
;.equ blinky,0
;.equ user_led,1
;.equ tx_status,2
;.equ tx_data,3
;.equ rx_status,4
;.equ rx_data,5
;.equ image,6
;.equ boot,7

.window                 ; todo this macro needs to align to 8 word boundary
J init
leds: .alloc 1
padStatus: .alloc 1      ; is the pad ready to go ?
padCount: .alloc 1       ; cursor for the pad
padCursor: .alloc 1       ; current position in the pad 
; pad itself is declared at the bottom so it does not overwrite code 
.equ delay,65000        ; constant for delay

; Basic echo construct
; Need macros and register renames
init:                           ; initialize the program all the registers.
    MOVI R0,0 ; working register        
    MOVI R1,10 ; working address 
    MOVI R2,20 ; holding data 
    MOVI R3,30 ; device status
    MOVI R4,40 ; delayer
    MOVI R5,50 ; temp 
    MOVI R6,60 ; jump2 return address
    MOVI R7,70 ; jump return address

    ; write the greet string
run:                                   ; main loop
    MOVR R1,greet
    JAL R6,nextchar
J run

txchar:                         ; put a char into the serial port 
    STXA R2,tx_data             ; put the holding data into the serial port
JR R7,0

nextchar:
    LD   R2,R1,0        ; load the data at working address into holding
    STXA R1,blinky
    JAL   R7,txchar      ; write the char
    ADDI R1,R1,1        ; increment the pointer
    CMPI R2,0           ; look for a null (0) 
    JNE  nextchar     ; not there yet, get next char
JR R6,0 ; return with jump2

greet: .string "Boneless-v3-zignig-bootloader"
pwd: .string ">>"
