from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto

from .diagnostics import SourceSpan


class TokenKind(Enum):
    KW_INT = auto()
    KW_MAIN = auto()
    KW_RETURN = auto()
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    SEMICOLON = auto()
    INTEGER = auto()
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    EOF = auto()


@dataclass(frozen=True, slots=True)
class Token:
    kind: TokenKind
    lexeme: str
    span: SourceSpan
    integer_value: int | None = None
