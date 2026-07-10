from __future__ import annotations

from .ast_nodes import BinaryExpr, Expression, NumberExpr, Program, UnaryExpr
from .diagnostics import CompileError
from .tokens import TokenKind


def validate_program(program: Program) -> None:
    _validate_expression(program.function.body.expression, negated=False)


def _validate_expression(expression: Expression, *, negated: bool) -> None:
    if isinstance(expression, NumberExpr):
        if expression.value == 2_147_483_648 and not negated:
            raise CompileError("positive integer literal exceeds INT32_MAX", expression.span)
        return

    if isinstance(expression, UnaryExpr):
        _validate_expression(
            expression.operand,
            negated=not negated if expression.operator is TokenKind.MINUS else negated,
        )
        return

    assert isinstance(expression, BinaryExpr)
    _validate_expression(expression.left, negated=False)
    _validate_expression(expression.right, negated=False)
    if expression.operator is TokenKind.SLASH and _evaluate_constant(expression.right) == 0:
        raise CompileError("division by zero", expression.right.span)


def _evaluate_constant(expression: Expression) -> int | None:
    try:
        if isinstance(expression, NumberExpr):
            value = expression.value
        elif isinstance(expression, UnaryExpr):
            operand = _evaluate_constant(expression.operand)
            if operand is None:
                return None
            value = operand if expression.operator is TokenKind.PLUS else -operand
        else:
            left = _evaluate_constant(expression.left)
            right = _evaluate_constant(expression.right)
            if left is None or right is None:
                return None
            if expression.operator is TokenKind.PLUS:
                value = left + right
            elif expression.operator is TokenKind.MINUS:
                value = left - right
            elif expression.operator is TokenKind.STAR:
                value = left * right
            elif expression.operator is TokenKind.SLASH:
                if right == 0:
                    return 0
                value = abs(left) // abs(right)
                if (left < 0) ^ (right < 0):
                    value = -value
            else:
                return None

        return value if -(2**31) <= value <= 2**31 - 1 else None
    except ArithmeticError:
        return None
