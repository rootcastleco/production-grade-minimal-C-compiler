from __future__ import annotations

from dataclasses import dataclass
from typing import TypeAlias

from .diagnostics import SourceSpan
from .tokens import TokenKind


@dataclass(frozen=True, slots=True)
class NumberExpr:
    value: int
    span: SourceSpan


@dataclass(frozen=True, slots=True)
class UnaryExpr:
    operator: TokenKind
    operand: Expression
    span: SourceSpan


@dataclass(frozen=True, slots=True)
class BinaryExpr:
    operator: TokenKind
    left: Expression
    right: Expression
    span: SourceSpan


Expression: TypeAlias = NumberExpr | UnaryExpr | BinaryExpr


@dataclass(frozen=True, slots=True)
class ReturnStatement:
    expression: Expression
    span: SourceSpan


@dataclass(frozen=True, slots=True)
class FunctionDefinition:
    name: str
    body: ReturnStatement
    span: SourceSpan


@dataclass(frozen=True, slots=True)
class Program:
    function: FunctionDefinition
    span: SourceSpan
