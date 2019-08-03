; \Build a forth in Assembly
; Simon Kirkby
; obetgiantrobot@gmail.com
; 20190319

.alloc stack, 8 ; .alloc will label and zero X cells;
.alloc rstack, 8

; redefine the registers

.def W, R0 ; working register
.def IP, R1 ; interpreter pointer
.def PSP, R2 ; parameter stack pointer 
.def TOS, R7 ; top of parameter stack
.def RSP, R4 ; return stack pointer 
.def JUMP, R5 ; jump saver , no direct access to PC
.def SP, R6 ; spare register 2
.def RTN, R3 ; cpu jump store

; macro to send an external halt to the simulator
.macro HALT 
    STX SP,SP,1
.endm

reset:
    MOVL PSP,15 
    MOVL RSP,23
    J init

abort:
    J init

; short form 
.macro _call, name
    JAL RTN, $name
.endm

.macro _ret 
    JR RTN, 0
.endm

; stack structures
.macro pop
;_call POP
    MOV W, TOS
    ADDI PSP, 1
    LD TOS,PSP, 0
.endm

.macro push
;_call PUSH
    ST TOS, PSP, 0
    SUBI PSP, 1
    MOV TOS, W
.endm

.macro rpop
;    _call RPOP
    LD W, RSP, 0 
    ADDI RSP, 1
.endm

.macro rpush
;    _call RPUSH
    ST W, RSP, 0 
    SUBI RSP, 1
.endm

; start of low level forth words

.equ latest, r_R0 ; start latest at the bottom of the cookie jat.
;
.macro HEADER, name     ; this makes a full header
; this is all python macros found in commands.py
    .plabel $name, d ; push a header label
    .pos latest         ; add current pos to code
    .pset latest, $name, d  ; copy this ref for next header
    .ulstring $name     ; unlabeled string length then characters
    .plabel $name , xt  ; the execution token , direct pointer
; this is a trick , registers the actual name as a marcro
; so you can write assembly in forth
    .mlabel $name ; make a direct execution macro , used later
.endm

; the inner interpreter

; --8<--  SNIP

; REF  http://www.figuk.plus.com/build/heart.htm
; NEEDED words NEXT , ENTER , EXECUTE , EXIT
; NEXT and ENTER are code fragments , use macros 
; EXECUTE and EXIT are forth words in assembly

; NEXT FRAGMENT
; [ip] to W IP++  [W] jump
.macro NEXT
    LD W,IP,0
    ADDI IP,1
    JR W,0
.endm

; ENTER FRAGMENT
.macro ENTER
    MOV W,IP    ; move the existing instruction pointer into working
    rpush       ; save where we are
    LD W,W,0    ; resolve the current instruction
    ADDI W,1    ; move to the next one  
    LD IP,W,0   ; save it for exit
    NEXT        ; and go;       
.endm

(DOCOL):
    push
    MOV W,IP
    rpush
    pop
    NEXT

.macro DOCOL
    .@ (DOCOL)
.endm

; EXECUTE FORTH WORD
HEADER EXECUTE
    pop 
    LD IP,W,0
    JR W,0
NEXT

; EXIT FORTH WORD
HEADER EXIT
    rpop
    MOV IP,W
    NEXT
NEXT

HEADER MAIN
    loop:
        .@  xt_ok
        .@  xt_ok
        .@  xt_ok
        .@  xt_ok
    .@ loop
NEXT

init:
    MOVA IP, xt_MAIN ; load the pointer for MAIN
    LD W,IP,0      ; put it into the instruction pointer
    JR W,0      ; go there 
J init

HEADER ok ; output ok
    MOVL W,111
    STX W,SP,0
    MOVL W,107
    STX W,SP,0
NEXT

HEADER halt  ; send halt up to the simulator
    STX SP,SP,1
NEXT

;HEADER ?key
;    NOP
;again:
;    LDX W,SP,0
;    CMP W,SP
;    JZ out
;    STX W,SP,0
;    J again
;out:
;    HALT
;NEXT

; Add all the prospective includes in
; .include asm/basic.asm
; .include asm/compiler.asm
; .include asm/intepreter.asm
; .include asm/other.asm

HEADER HERE
    .pos latest
NEXT
