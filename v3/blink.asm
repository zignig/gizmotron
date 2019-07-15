.window
; comment
init:                           ; start here 
        MOVI    R0,0            ; move zero into R0
        MOVI    R1,0            ; move zerp into R1
entry:
        ADDI    R0,R0, 1 	; add one to R0 ( increment the leds )
	STXA	R0, 0           ; write to the leds 
wait:
        ADDI    R1,R1,1         ; add 1 to the counter
        CMPI    R1,50000        ; is the counter 50,000 ?
        JNE     wait            ; not there yet jump back
        MOVI    R1,0            ; reset R1 to zero
	J	entry           ; start again , increment the leds
