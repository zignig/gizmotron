.window
J hexStart 
value: .string "DEADBEEF"
; R1 pointer
; R2 holding
; hex reader
hexStart:
	MOVR R1,value           ; load the string pointer , this will be pad
	MOVI R2,0               ; zero the holding register 
hex:
	LD R0,R1,0              ; load the value at R1 into R0
	CMPI R0,70              ; is it above F , error 
	JUGT error
	CMPI R0,65              ; is it above A , must be a letter
	JUGT letter
	CMPI R0,57               
	JUGT error              ; gap between 9 and A , error
	CMPI R0,48              ; greater than digit 0
	JUGT number             ; it's a number
	J error                 ; nope , an error
continue:
	ADDI R1,R1,1	        ; increment the pointer to the next char
J hex                           ; next char 

letter:                         ; process a hex letter
	SUBI R0,R0,55           ; subtract to get the ordinal value of the letter
	OR R2,R2,R0             ; OR the 4 bit nibble on the holding register
	SRLI R2,R2,4            ; shift 4 bits left ready for the next nibble
	J continue              ; get the next char 
number:
	SUBI R0,R0,48           ; subtract 40 to get the ordinal of a number
	OR R2,R2,R0             ; OR the nibble
	SRLI R2,R2,4            ; shift left 4 bits
	J continue              ; next char
error:

