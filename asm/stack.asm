; stack allocation and functions


; allocate some stack storage 
.equ stack_size,16 ; make a constant for the stack size
.alloc stack,stack_size  ; allocate 16 words for the stack
.alloc return_stack,stack_size

.macro push,reg
.endm

.macro pop,reg
.endm
