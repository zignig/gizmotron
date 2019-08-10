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
    MOVI R1,0 ; working address 
    MOVI R2,0 ; holding data 
    MOVI R3,0 ; device status
    MOVI R4,0 ; delayer
    MOVI R5,0 ; temp 
    MOVI R6,0 ; jump2 return address
    MOVI R7,0 ; jump return address

    ; write the greet string
run:                                   ; main loop
    MOVR R1,greet
    JAL R6,nextchar
    JAL R7,countup
J run

countup:
    ADDI R0,R0,1
JR R7,0

txchar:                         ; put a char into the serial port 
    STXA R2,tx_data             ; put the holding data into the serial port
    MOVI R3,1                   ; set status to one
    STXA R3,tx_status           ; write to tx status 
    MOVI R3,0                   ; set the status to zero
    STXA R3,tx_status           ; acknowledge the write 
waitup:                         ; TODO , this should be a fifo in the serial port 
    LDXA R3,tx_status           ; wait for tx status to go high
    CMPI R3,1
    JE waitup
waitdown:
    LDXA R3,tx_status           ; wait for the status to go low
    CMPI R3,0
    JE waitdown
JR R7,0

;txchar:                         ; put a char into the serial port 
;    STXA R2,tx_data             ; put the holding data into the serial port
;JR R7,0

nextchar:
    LD   R2,R1,0        ; load the data at working address into holding
    JAL   R7,txchar      ; write the char
    ADDI R1,R1,1        ; increment the pointer
    CMPI R2,0           ; look for a null (0) 
    JNE  nextchar     ; not there yet, get next char
JR R6,0 ; return with jump2

greet: .string "Text thing"
