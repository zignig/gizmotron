.window
J init
value: .string "DEADBEEF"
; R2 holding
init:
	MOVR R1,value
	MOVI R2,0 
hex:
	LD R0,R1,0
	CMPI R0,70 ; F
	JUGT error
	CMPI R0,65 ; A
	JUGT letter
	CMPI R0,57 
	JUGT error ; gap
	CMPI R0,48
	JUGT number
	J error
continue:
	ADDI R1,R1,0	
J hex 

letter:
	SUBI R0,R0,55
	OR R2,R2,R0
	SRLI R2,R2,4
	J continue 
number:
	SUBI R0,R0,48
	OR R2,R2,R0
	SRLI R2,R2,4
	J continue 
error:

