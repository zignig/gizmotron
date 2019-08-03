.include asm/stack.asm
J init ; jump to init


.def data , R0		; makes an alias for a register 
.def addr , R1
.def char , R2
.def d2 , R4
.def zero , R6
.def one, R5
.def rtn, R7
.def max,R3

; creates a string with the word add the address holding the length
.string test,"this is a longer string to see if this works"
.string cls,"\u001b[38;5;"
; create a place to put the incoming characters
.alloc pad,64
.alloc pad_p,1

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
	LDX d2,addr,0
.endm

; copy serial data into data register
; ----- RX macros
.macro get_rx_data
        MOVI addr,rx_data
        LDX data,addr,0
.endm

.macro ack_rx_status, value
	MOVI addr,rx_status
	MOVI d2,$value
	STX d2,addr,0	
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
	LDX d2,addr,0
.endm

.macro ack_tx_status, value
	MOVI addr,tx_status
	MOVI d2,$value
	STX d2,addr,0	
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
    CMP d2,one
    JE wait_up
_return

; wait for a key press
wait_key:
    get_rx_status 
    CMP d2,zero
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

; main loop
init:
    MOVI one,1
loop:
    _call wait_key
    write_leds
    _call put_char
J loop

