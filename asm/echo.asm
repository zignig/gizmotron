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
spacer: .alloc 500
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
    MOVR R1,nl
    JAL R6,nextchar
    MOVR R1,greet
    JAL R6,nextchar
    MOVR R1,pwd
    JAL R6,nextchar
run:                                   ; main loop
    JAL R7,checkrx                     ; get a char from the serial port
    JAL R7,txchar                      ; write R2 ( holding ) to the serial port 
    J procpad		       ; check pad active and process
J run

warmboot:
    MOVR R1,wb
    JAL R6,nextchar
    MOVI R0,1
    STXA R0,image
    MOVI R0,1
    STXA R0,boot

checkrx:                        ; get a char off the serial port 
    LDXA R3,rx_status           ; load the RX status from the serial port
    CMPI R3,1                   ; compare the register to 1
    JE addtopad                 ; if it is equal to one ,  add it to the pad
    J checkrx
addtopad:
    ; get the data and acknowledge
    LDXA R2,rx_data             ; load the RX data from the serial port
    MOVI R3,1                   ; load 1 into to R3
    STXA R3,rx_status           ; acknowledge the char in the serial port
    MOVI R3,0                   ; load 0 into to R3
    STXA R3,rx_status           ; acknowledge the char in the serial port
    CMPI R2,4
    JE warmboot
    ; check if it is a ^C
    CMPI R2,3
    JE init
    ; check if it is a CR and set the padstatus to 1
    CMPI R2,13                  ; is a CR
    JNE padContinue
    ; update the pad status to 1
    MOVR R1,padStatus
    MOVI R0,1
    ST R0,R1,0
    JR R7,0
padContinue:
    ; put the incoming char into the pad
    MOVR R1,pad		 ; move pad into the working address
    LD R0,R1,0		 ; load the length into the working register
    AND R5,R1,R1	 ; copy the padd address into holding
    ADD R5,R5,R0	 ; add the current pad length to holding
    ST R2,R5,0		 ; store the word into to address in holding
    ADDI R0,R0,1	 ; increment to pad count
    ST R0,R1,0		 ; store the value back into the start of the pad
JR R7,0


txchar:                         ; put a char into the serial port 
    STXA R2,tx_data             ; put the holding data into the serial port
    STXA R2,blinky
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


nextchar:
    LD   R2,R1,0        ; load the data at working address into holding
    JAL   R7,txchar      ; write the char
    ADDI R1,R1,1        ; increment the pointer
    CMPI R2,0           ; look for a null (0) 
    JNE  nextchar     ; not there yet, get next char
JR R6,0 ; return with jump2

dumppad: ; just dump the pad to console
    ; TODO
JR R6,0
    
procpad:
    MOVR R1,padStatus	; load the pad status address into R1
    LD R0,R1,0		; load the pad status into R0
    CMPI R0,1		; is the pad active
    JE procPadContinue  ; continue
    J run
procPadContinue:
    ; process the pad here 
     
    ; TODO write pad
    JAL R6,dumppad
    MOVR R1,nl          ; write a newline
    JAL R6,nextchar     
    MOVR R1,pwd         ; write the console prompt
    JAL R6,nextchar
    MOVR R1,padStatus   ; reset pad status 
    MOVI R0,0
    ST R0,R1,0
J run
    
greet: .string "Boneless-v3-zignig-bootloader\r\n"
nl: .string "\r\n"
pwd: .string "$ "
wb: .string "!warmboot"
; add strings various here
pad: .alloc 32 ; the pad itself 
