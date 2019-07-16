; basic echo 
.window 
.def 	bob,4

.macro bill 
	LDXA R1,1
.endm 

.macro gorm 
	LDXA R1,$gorm
.endm

J init
; R0 = data
; R1 = char
; R7 = return address

waitrxchar: 		; wait for a char on serial 
	LDXA R0,1	; load the rx status
	CMPI R0,1	; is it 1
	JZ waitrxchar	; if 
	LDXA R1,2	; load the data into chear 
	JR R7,0		; return from the sub 

txchar:			; transmit a char
	STXA R1,4	; store the char in the output regiter 
	MOVI R0,1	; 
	STXA R0,bob
; Main Loop
waittxack:
	LDXA R2,3
	CMPI R2,1
	JE waittxack
init:
	JAL R7,waitrxchar
J init
