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
.def status , R3
.def status_c, R4
.def hold,R5
.def rtn_p,R6
.def rtn, R7

.alloc return_stack,8
.alloc count,1
.alloc start_addr,1
.alloc data_temp,1
.alloc checksum,1

; helper functions for call and return
.macro _call, jump
    ADDI rtn_p,1
    ST rtn,rtn_p,0
    JAL rtn,$jump
    LD rtn,rtn_p,0
    SUBI rtn_p,1
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
    NOP
    MOVI rtn_p,@return_stack
loop:
    _call colon
J loop

.macro get_hex_char
	_call wait_key
	_call hex_digit
.endm

get_count:
	get_hex_char
	get_hex_char
_return

get_address:
	get_hex_char
	get_hex_char
	get_hex_char
	get_hex_char
_return 

; put the data register onto the uart and wait.
put_char:
    put_tx_data data
    set_ack
    clear_ack
wait_up:
    get_tx_status
    MOVI status_c,1
    CMP status,status_c
    JE wait_up
_return

; wait for a key press
wait_key:
    get_rx_status 
    MOVI status_c,0
    CMP status,status_c
    JNE is_key 
    J wait_key
is_key:
    get_rx_data
    set_rx_ack
    clear_rx_ack
_return 

colon:
        _call wait_key
	compare 58
	JNE error
	; starts with a colon
	MOVI hold,0
	_call get_count
	; put into count
	MOVI addr,@count
	ST hold,addr,0
	; get address 
	MOVI hold,0
	_call get_address
	; put address into addr
	MOVI addr,@start_addr
	ST hold,addr,0
	; have address count
next_data:
	MOVI hold,0
	_call get_address ; this is data this time
	MOVI addr,@data_temp
	ST hold,addr,0
	; put the data into place
;	MOVI addr,@data_temp
;	LD char,addr,0
;	MOVI addr,@start_addr
;	ST char,addr,0
	MOVI addr,@count
	LD data,addr,0
	SUBI data,4
	ST data,addr,0
	MOVI status,0
	CMP data,status
	JNZ next_data
_return 

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
	SUBI char,55 ; subtract to get number
	shift hold
_return

number:
	MOV char,data
	SUBI char,48
	shift hold
_return

error:
	MOVI data,33
	_call put_char		
_return
