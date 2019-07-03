; Serial bootloader
; Use intex hex format seems to be common denominator
.equ user_leds,0
.equ tx_status,1
.equ tx_data,2
.equ rx_status,3
.equ rx_data,4

J init ; jump to init


.def data , R0		; makes an alias for a register 
.def addr , R1
.def char , R2
.def status , R4
.def zero , R6
.def one, R5
.def rtn, R7
.def hold,R3

; helper functions for call and return
.macro _call, jump
    JAL rtn,$jump
.endm

.macro _return
    JR rtn,0
.endm

; helper macros for talking to the primary serial port 
.macro get_rx_status
	MOVI addr,rx_status
	LDX status,addr,0
.endm

; copy serial data into data register
; ----- RX macros
.macro get_rx_data
        MOVI addr,rx_data
        LDX data,addr,0
.endm

.macro ack_rx_status, value
	MOVI addr,rx_status
	MOVI status,$value
	STX status,addr,0	
.endm

.macro set_rx_ack
	ack_rx_status 1
.endm

.macro clear_rx_ack
	ack_rx_status 0
.endm

; ------ TX macros
.macro get_tx_status
	MOVI addr,tx_status
	LDX status,addr,0
.endm

.macro ack_tx_status, value
	MOVI addr,tx_status
	MOVI status,$value
	STX status,addr,0	
.endm

.macro set_ack
	ack_tx_status 1
.endm

.macro clear_ack
	ack_tx_status 0
.endm

.macro put_tx_data, data
	MOVI addr,tx_data
	MOV data,$data
	STX data,addr,0
.endm

; put the data register onto the uart and wait.
put_char:
    put_tx_data data
    set_ack
    clear_ack
wait_up:
    get_tx_status
    CMP status,one
    JE wait_up
_return

; wait for a key press
wait_key:
    get_rx_status 
    CMP status,zero
    JNE is_key 
    J wait_key
is_key:
    get_rx_data
    set_rx_ack
    clear_rx_ack
_return 

; end serial helpers

; send data to the userleds
.macro write_leds
        MOVI addr,user_leds
        STX data,addr,0
.endm

.macro shift,reg
	SLL $reg,$reg,4
	OR $reg,$reg,char
.endm

.macro compare,val
	MOVI char,$val
	CMP data,char
.endm 

; main loop
init:
    MOVI one,1
loop:
    _call wait_key
    _call hex_digit
J loop


hex_digit:
	compare 70 ; F
	JUGT error ; hex digit is out of range
	compare 65 ; A
	JUGE letter
	compare 57 ; 9
	JUGT error  ; in the gap between 9 and A ,error	
	compare 48 ; 0
	JUGE number
	J error
letter:
	MOV char,data
	SUBI char,55; subtract to get number
	shift hold
_return

number:
	MOV char,data
	SUBI char,48
	shift hold
_return

error:
	MOVI char,33
	MOVI addr,tx_data
	STX char,addr,0
	set_ack
	clear_ack
wait_up2:
	get_tx_status
	CMP status,one
	JE wait_up2
J loop 
