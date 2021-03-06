; automatic gizmo headers
;.equ blinky,0
;.equ user_led,1
;.equ tx_status,2
;.equ tx_data,3
;.equ rx_status,4
;.equ rx_data,5
;.equ image,6
;.equ boot,7
.equ bottom, 32
.equ top, 126
.equ counter,1000

base: .window                 ; todo this macro needs to align to 8 word boundary
J init

txchar:                         ; put a char into the serial port 
    STXA R2,tx_data             ; put the holding data into the serial port
    STXA R2,blinky              ; put the holding data into the serial port
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

init:
    MOVI R4,0
run:
    ADDI R2,R2,1
    ADDI R1,R1,1
    JAL  R7,txchar
    CMPI R1,counter
    JE up 
    CMPI R2,top
    JULE run
    MOVI R2,bottom
J run        
up:
    MOVI R2,bottom
    MOVI R1,0
    ADDI R4,R4,1
    CMPI R4,20
    JE warmme
J run
warmme:
    MOVI R0,1                   ; set boot image to 1
    STXA R0,image               ; write to the image external register
    MOVI R0,1                   ; write one into regiters
    STXA R0,boot                ; reboot the FPGA into the boot loader
