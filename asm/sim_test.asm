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
.equ delay,65000        ; constant for delay

init:                           ; initialize the program all the registers.
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
JR R7,0

nextchar:
    LD   R2,R1,0        ; load the data at working address into holding
    JAL   R7,txchar      ; write the char
    ADDI R1,R1,1        ; increment the pointer
    CMPI R2,0           ; look for a null (0) 
    JNE  nextchar     ; not there yet, get next char
JR R6,0 ; return with jump2

greet: .string "Text thing"
