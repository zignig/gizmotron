J init
; Some delay macros 

.equ tx_status,1
.equ tx_data,2

.def data , R0
.def addr , R1

.macro get_tx_status
	MOVI addr,tx_status
	LDX data,addr,0
.endm

.macro put_tx_data
	MOVI addr,tx_data
	STX data,addr,0
.endm

init:
    MOVI R4,49
    MOVI R5,60
loop:
    NOP
wait:
    LDX R6, R1,0
    CMP R3,R6
    JE wait
    MOV R4,R1
    put_tx_data
    J loop

