global _start
section .text

_start:
    call main
    mov edi, eax        ; status = main()
    mov eax, 60         ; Linux x86-64 sys_exit
    syscall

main:
    mov eax, 7
    push rax
    mov eax, 5
    mov ecx, eax        ; right operand
    pop rax             ; left operand
    add eax, ecx
    push rax
    mov eax, 3
    mov ecx, eax        ; right operand
    pop rax             ; left operand
    imul eax, ecx
    push rax
    mov eax, 2
    mov ecx, eax        ; right operand
    pop rax             ; left operand
    cdq                 ; sign-extend eax into edx:eax
    idiv ecx            ; eax = quotient, edx = remainder
    push rax
    mov eax, 4
    mov ecx, eax        ; right operand
    pop rax             ; left operand
    sub eax, ecx
    ret
