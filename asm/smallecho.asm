; Bootloader Console
; Simon Kirkby
; 20190822
; obeygiantrobot@gmail.com


; automatic gizmo headers
;.equ blinky,0
;.equ user_led,1
;.equ tx_status,2
;.equ tx_data,3
;.equ rx_status,4
;.equ rx_data,5
;.equ image,6
;.equ boot,7

base: .window                 ; todo this macro needs to align to 8 word boundary
win: .window            ; named window , this is hand aligned to *8
J init                  ; jump to init
reboot:                ; label for rebooting into

init:                           ; initialize the program all the registers.
    MOVI R0,base
    STW  R0                     ; set the register window at zero 

run:                            ; main loop
    JAL R7,checkrx              ; get a char from the serial port
    JAL R7,txchar               ; write R2 ( holding ) to the serial port 
J run

warmboot:
    MOVI R0,0                   ; set boot image to 0
    STXA R0,image               ; write to the image external register
    MOVI R0,1                   ; write one into regiters
    STXA R0,boot                ; reboot the FPGA into the boot loader

checkrx:                        ; get a char off the serial port 
    LDXA R3,rx_status           ; load the RX status from the serial port
    CMPI R3,1                   ; compare the register to 1
    BEQ addtopad                ; if it is equal to one ,  add it to the pad
    J checkrx
addtopad:                       ; get the data and acknowledge
    MOVI R3,1                   ; load 1 into to R3
    STXA R3,rx_status           ; acknowledge the char in the serial port
    MOVI R3,0                   ; load 0 into to R3
    STXA R3,rx_status           ; acknowledge the char in the serial port
continue:
    LDXA R2,rx_data             ; load the RX data from the serial port
    STXA R2,blinky
    CMPI R2,4                   ; check if it is ^D , warmboot
    BEQ warmboot                  

JR R7,0                     ; jump to main


txchar:                         ; put a char into the serial port 
    STXA R2,tx_data             ; put the holding data into the serial port
    MOVI R3,1                   ; set status to one
    STXA R3,tx_status           ; write to tx status 
    MOVI R3,0                   ; set the status to zero
    STXA R3,tx_status           ; acknowledge the write 
;waitup:                         ; TODO , this should be a fifo in the serial port 
;    LDXA R3,tx_status           ; wait for tx status to go high
;    CMPI R3,1
;    BEQ waitup
;waitdown:
;    LDXA R3,tx_status           ; wait for the status to go low
;    CMPI R3,0
;    BEQ waitdown
JR R7,0
