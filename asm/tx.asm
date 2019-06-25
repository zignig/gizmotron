J init
; Some delay macros 


.equ tx_status,1
.equ tx_data,2

.def data , R0
.def addr , R1
.def d2 , R4
.def zero , R6
.def max,R3

.string test,"this is a longer string to see if this works"

.macro get_tx_status
	MOVI addr,tx_status
	LDX data,addr,0
.endm

.macro ack_tx_status, value
	MOVI addr,tx_status
	MOVI data,$value
	STX data,addr,0	
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

init:
    MOVI d2,49
    MOVI max,55
    clear_ack 
loop:
    NOP
wait:
    get_tx_status
    CMP data,zero
    JE wait
    put_tx_data d2
    set_ack
    ADDI d2,1
    CMP d2,max
    JE init
    J loop

