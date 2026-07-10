from __future__ import annotations

from .ast_nodes import BinaryExpr, Expression, NumberExpr, Program, UnaryExpr
from .diagnostics import CodegenError
from .tokens import TokenKind


class X86_64CodeGenerator:
    def __init__(self) -> None:
        self.lines: list[str] = []
        self.stack_depth = 0

    def generate(self, program: Program) -> str:
        self.lines = [
            "global _start",
            "section .text",
            "",
            "_start:",
            "    call main",
            "    mov edi, eax        ; status = main()",
            "    mov eax, 60         ; Linux x86-64 sys_exit",
            "    syscall",
            "",
            "main:",
        ]
        self._emit_expression(program.function.body.expression)
        if self.stack_depth != 0:
            raise CodegenError("internal error: unbalanced expression stack")
        self.lines.extend(("    ret", ""))
        return "\n".join(self.lines)

    def _emit_expression(self, expression: Expression) -> None:
        if isinstance(expression, NumberExpr):
            immediate = expression.value
            self.lines.append(
                "    mov eax, 0x80000000"
                if immediate == 2_147_483_648
                else f"    mov eax, {immediate}"
            )
            return

        if isinstance(expression, UnaryExpr):
            self._emit_expression(expression.operand)
            if expression.operator is TokenKind.MINUS:
                self.lines.append("    neg eax")
            elif expression.operator is not TokenKind.PLUS:
                raise CodegenError("unsupported unary operator", expression.span)
            return

        if not isinstance(expression, BinaryExpr):
            raise CodegenError("unknown AST node")
        self._emit_binary(expression)

    def _emit_binary(self, expression: BinaryExpr) -> None:
        self._emit_expression(expression.left)
        self.lines.append("    push rax")
        self.stack_depth += 8
        self._emit_expression(expression.right)
        self.lines.extend(
            (
                "    mov ecx, eax        ; right operand",
                "    pop rax             ; left operand",
            )
        )
        self.stack_depth -= 8

        instruction = {
            TokenKind.PLUS: "add eax, ecx",
            TokenKind.MINUS: "sub eax, ecx",
            TokenKind.STAR: "imul eax, ecx",
        }.get(expression.operator)
        if instruction is not None:
            self.lines.append(f"    {instruction}")
            return

        if expression.operator is TokenKind.SLASH:
            self.lines.extend(
                (
                    "    cdq                 ; sign-extend eax into edx:eax",
                    "    idiv ecx            ; eax = quotient, edx = remainder",
                )
            )
            return

        raise CodegenError("unsupported binary operator", expression.span)
