; tiny bootloader 
; Simon Kirkby
; 20190830
; obeygiantrobot@gmail.com
; automatic gizmo headers
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

spacer: .alloc 512      ; spacer for the new program , asm needs to be able to link to the bottom

init:                           ; initialize the program all the registers.
    MOVI R0,base
    STW  R0                     ; set the register window at zero 
run:                            ; main loop
    JAL R7,checkrx              ; get a char from the serial port
J run

warmme:
    MOVI R0,1                   ; set boot image to 1
    STXA R0,image               ; write to the image external register
    MOVI R0,1                   ; write one into regiters
    STXA R0,boot                ; reboot the FPGA into the boot loader

checkrx:                        ; get a char off the serial port 
    LDXA R3,rx_status           ; load the RX status from the serial port
    CMPI R3,1                   ; compare the register to 1
    JE nextchar 		; if it is equal to one ,  add it to the pad
    J checkrx
nextchar:
    LDXA R2,rx_data             ; load the RX data from the serial port
    MOVI R3,1                   ; load 1 into to R3
    STXA R3,rx_status           ; acknowledge the char in the serial port
    MOVI R3,0                   ; load 0 into to R3
    STXA R3,rx_status           ; acknowledge the char in the serial port
    CMPI R2,70              ; is it above F , error 
    JUGT hexerror
    CMPI R2,65              ; is it above A , must be a letter
    JUGE letter
    CMPI R2,57               
    JUGT hexerror              ; gap between 9 and A , error
    CMPI R2,48              ; greater than digit 0
    JUGE number             ; it's a number
    J hexerror                  ; nope , an error
continue:
    CMP  R1,R5                  ; compare current with end of string
    JE copytomem 
    J hexnext
copytomem:
    ; R4 should contain the decoded hex value
    CMPI R4,0xFFFF                   ; if the string is FFFF boot into it
    JE bootinto 
    
    MOVR R1,addr                ; load the working address
    LD R0,R1,0                  ; load the value
    ST R4,R0,0                  ; store the working data into the address
    ADDI R0,R0,1                ; increment the pointer
    ST R0,R1,0                  ; put it back into addr
J nextcommand


letter:                         ; process a hex letter
    SUBI R2,R2,55               ; subtract to get the ordinal value of the letter
    J nextnibble
number:
    SUBI R2,R2,48           ; subtract 40 to get the ordinal of a number
nextnibble:
    SLLI R4,R4,4            ; shift left 4 bits
    OR R4,R4,R2             ; OR the nibble
J continue              ; next char

bootinto:
    MOVR R1,boottext
    JAL R6,dumpstring           ; write the boot string
    MOVI R0,win
    STW  R0                     ; set the register window at zero 
    J  reboot

hexerror:
    MOVI R2,33 			; ! char
    JSR txchar,R7
    J init
    
txchar:                         ; put a char into the serial port 
    STXA R2,tx_data             ; put the holding data into the serial port
    STXA R2,blinky              ; into blinky
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
