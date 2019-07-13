	.word 0
	.word 0
	.word 0
	.word 0
	.word 0
	.word 0
	.word 0
	.word 0
entry:
        ADDI    R0,R0, 1 	
	STXA	R0, 0
wait:
        ADDI    R1,R1,1
        CMPI    R1, 9000 
        JNE wait 
	J	entry
