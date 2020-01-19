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
    MOVI R0,0 ; working register        
    MOVI R1,0 ; working address 
    MOVI R2,0 ; holding data 
    MOVI R3,0 ; device status
    MOVI R4,0 ; current bootloader write data 
    MOVI R5,0 ; end of string address
    MOVI R6,0 ; jump2 return address , no return stack , careful with the return registers
    MOVI R7,0 ; jump return address

    ; write the greet string
    MOVR R1,nl                  ; newline
    JAL R6,dumpstring
    MOVR R1,greet               ; greetings string
    JAL R6,dumpstring
    MOVR R1,pwd                 ; prompt
    JAL R6,dumpstring

    MOVR R1,pad                 ; load the pad address
    MOVI R0,0                   ; load a zero
    ST R0,R1,0                  ; store the zero in the pad length cell

    MOVR R1,padStatus           ; reset the pad status  
    MOVI R0,0 
    ST R0,R1,0

run:                            ; main loop
    JAL R7,checkrx              ; get a char from the serial port
    JAL R7,txchar               ; write R2 ( holding ) to the serial port 
    J procpad		        ; check pad active and process
J run

warmboot:
    MOVR R1,wb                  ; write the warmboot string to the console
    JAL R6,dumpstring
    MOVI R0,0                   ; set boot image to 0
    STXA R0,image               ; write to the image external register
    MOVI R0,1                   ; write one into regiters
    STXA R0,boot                ; reboot the FPGA into the boot loader

warmme:
    MOVI R0,1                   ; set boot image to 1
    STXA R0,image               ; write to the image external register
    MOVI R0,1                   ; write one into regiters
    STXA R0,boot                ; reboot the FPGA into the boot loader

checkrx:                        ; get a char off the serial port 
    LDXA R3,rx_status           ; load the RX status from the serial port
    CMPI R3,1                   ; compare the register to 1
    BEQ addtopad                ; if it is equal to one ,  add it to the pad
    J checkrx
addtopad:                       ; get the data and acknowledge
    LDXA R2,rx_data             ; load the RX data from the serial port
    MOVI R3,1                   ; load 1 into to R3
    STXA R3,rx_status           ; acknowledge the char in the serial port
rxdown:
    LDXA R3,rx_status           ; load the RX status from the serial port
    STXA R3,blinky
    CMPI R3,0                   ; compare the register to 1
    BEQ rxcont                  ; if it is equal to zero continue 
    J rxdown 
rxcont:
    MOVI R3,0                   ; load 0 into to R3
    STXA R3,rx_status           ; acknowledge the char in the serial port

    CMPI R2,4                   ; check if it is ^D , warmboot
    BEQ warmboot                  

    CMPI R2,3                   ; check ^C restart processor
    BEQ warmme 

    ; check if it is a CR and set the padstatus to 1
    CMPI R2,13                  ; is a CR
    BNE padContinue
    ; update the pad status to 1
    MOVR R1,padStatus
    MOVI R0,1
    ST R0,R1,0
    JR R7,0
padContinue:
    ; put the incoming char into the pad
    MOVR R1,pad		        ; move pad into the working address
    LD R0,R1,0		        ; load the length into the working register
    ADDI R0,R0,1	        ; increment to pad count
    AND R5,R1,R1	        ; copy the pad address into holding
    ADD R5,R5,R0	        ; add the current pad length to holding
    ST R2,R5,0		        ; store the word into to address in holding
    ST R0,R1,0		        ; store the value back into the pad counter 
    JR R7,0                     ; jump to main


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
    BEQ waitup
waitdown:
    LDXA R3,tx_status           ; wait for the status to go low
    CMPI R3,0
    BEQ waitdown
    JR R7,0

; strings are pascal style strings,  first word is the length of the string. 
dumpstring:
    LD R0,R1,0                  ; load the length of the string into R0 
    CMPI R0,0                   ; empty string , go back
    BEQ exitdump
    AND R5,R1,R1                ; copy address into temp
    ADD R5,R5,R0                ; add the length to the address
    ; R1 is the current address
    ; R5 is the end of the string
nextchar:
    ADDI R1,R1,1                ; increment the pointer
    LD   R2,R1,0                ; load the data at working address into holding
    JAL  R7,txchar              ; write the char
    CMP  R1,R5                  ; compare current with end of string
    BLTU nextchar               ; not there yet, get next char
exitdump:
    JR R6,0                     ; return with jump2
    
; Process the pad
procpad:
    MOVR R1,padStatus	        ; load the pad status address into R1
    LD R0,R1,0		        ; load the pad status into R0
    CMPI R0,1		        ; is the pad active
    BEQ procPadContinue          ; continue
    J run                       ; return to run
procPadContinue:
    ; process the pad here 
    ; just dump to console for now 
    MOVR R1,nl                  ; write a newline
    JAL R6,dumpstring
    MOVR R1,pad                 ; write the pad
    JAL R6,dumpstring
    ; next command ...
nextcommand:
    MOVR R1,nl                  ; write a newline
    JAL R6,dumpstring
    MOVR R1,pwd                 ; write the console prompt
    JAL R6,dumpstring
    MOVR R1,padStatus           ; reset pad status 
    MOVI R0,0
    ST R0,R1,0
    MOVR R1,pad                 ; reset pad counter 
    MOVI R0,0
    ST R0,R1,0
J run                           ; back to main loop


greet: .string "Boneless-v3-zignig-bootloader\r\n"
nl: .string "\r\n"
pwd: .string ">> "
wb: .string "!warmboot"
next: .string "..."
error: .string "\r\n!Error"
boottext: .string "\r\nbooting..."

; add strings various here

; some variables 
padStatus: .alloc 1     ; is the pad ready to go ?
addr: .word 8 ; current address of the write bootloader writer
jump: .alloc 1 ; address to boot into
length: .alloc 1 ; length of the new firmware 
sequence: .alloc 1 ; the current mode of the bootloader 

; TODO what to do with the pad ? 
; get read hex running
; convert to number and write to memory
; jump to start 

pad: .alloc 32 ; the pad itself 
