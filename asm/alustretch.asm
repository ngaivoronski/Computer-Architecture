; Code to test the Sprint Challenge
;
; Expected output:
; 0
; 3
; 1
; -171
; 28
; 1
; 3

; TEST AND

LDI R0,0
LDI R1,1
AND R0,R1   ; Should AND to 0
PRN R0      ; Prints 0

; TEST OR

LDI R0,2
LDI R1,1
OR R0,R1    ; Should OR to 3
PRN R0      ; Prints 3

; TEST XOR

LDI R0,3
LDI R1,2
XOR R0,R1    ; Should XOR to 1
PRN R0      ; Prints 1

; TEST NOT

LDI R0,170
NOT R0      ; Should NOT 170 to -171
PRN R0      ; Prints -171

; TEST SHL
LDI R0,7
LDI R1,2
SHL R0,R1   ; Should shift 7 left by 2
PRN R0      ; Prints 28

; TEST SHR
LDI R0,7
LDI R1,2
SHR R0,R1   ; Should shift 7 right by 2
PRN R0      ; Prints 1

; TEST MOD
LDI R0,7
LDI R1,4
MOD R0,R1   ; Should 7 mod 4
PRN R0      ; Prints 3

; TEST ADDI
LDI R0,7
;ADDI R0,4   ; Should add 4 to R0
PRN R0      ; Prints 11

HLT