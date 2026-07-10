from __future__ import annotations

from .diagnostics import LexError, SourceLocation, SourceSpan
from .tokens import Token, TokenKind

_KEYWORDS = {
    "int": TokenKind.KW_INT,
    "main": TokenKind.KW_MAIN,
    "return": TokenKind.KW_RETURN,
}

_SINGLE_CHAR_TOKENS = {
    "(": TokenKind.LPAREN,
    ")": TokenKind.RPAREN,
    "{": TokenKind.LBRACE,
    "}": TokenKind.RBRACE,
    ";": TokenKind.SEMICOLON,
    "+": TokenKind.PLUS,
    "-": TokenKind.MINUS,
    "*": TokenKind.STAR,
    "/": TokenKind.SLASH,
}


class Lexer:
    def __init__(self, source: str) -> None:
        self.source = source
        self.index = 0
        self.line = 1
        self.column = 1

    def tokenize(self) -> list[Token]:
        tokens: list[Token] = []

        while not self._at_end():
            ch = self._peek()
            if ch.isspace():
                self._advance()
                continue
            if ch == "/" and self._peek_next() == "/":
                self._skip_line_comment()
                continue
            if ch == "/" and self._peek_next() == "*":
                self._skip_block_comment()
                continue
            if ch.isdigit():
                tokens.append(self._scan_integer())
                continue
            if ch.isalpha() or ch == "_":
                tokens.append(self._scan_identifier())
                continue

            token_kind = _SINGLE_CHAR_TOKENS.get(ch)
            if token_kind is not None:
                start = self._location()
                lexeme = self._advance()
                tokens.append(Token(token_kind, lexeme, SourceSpan(start, self._location())))
                continue

            start = self._location()
            bad_char = self._advance()
            raise LexError(f"invalid character {bad_char!r}", SourceSpan(start, self._location()))

        location = self._location()
        tokens.append(Token(TokenKind.EOF, "", SourceSpan(location, location)))
        return tokens

    def _scan_integer(self) -> Token:
        start = self._location()
        start_index = self.index
        while not self._at_end() and self._peek().isdigit():
            self._advance()

        lexeme = self.source[start_index:self.index]
        value = int(lexeme, 10)
        if value > 2_147_483_648:
            raise LexError(
                "integer literal is outside the supported 32-bit range",
                SourceSpan(start, self._location()),
            )
        return Token(TokenKind.INTEGER, lexeme, SourceSpan(start, self._location()), value)

    def _scan_identifier(self) -> Token:
        start = self._location()
        start_index = self.index
        while not self._at_end() and (self._peek().isalnum() or self._peek() == "_"):
            self._advance()

        lexeme = self.source[start_index:self.index]
        kind = _KEYWORDS.get(lexeme)
        if kind is None:
            raise LexError(f"unknown identifier {lexeme!r}", SourceSpan(start, self._location()))
        return Token(kind, lexeme, SourceSpan(start, self._location()))

    def _skip_line_comment(self) -> None:
        self._advance()
        self._advance()
        while not self._at_end() and self._peek() != "\n":
            self._advance()

    def _skip_block_comment(self) -> None:
        start = self._location()
        self._advance()
        self._advance()
        while not self._at_end():
            if self._peek() == "*" and self._peek_next() == "/":
                self._advance()
                self._advance()
                return
            self._advance()
        raise LexError("unterminated block comment", SourceSpan(start, self._location()))

    def _peek(self) -> str:
        return self.source[self.index]

    def _peek_next(self) -> str:
        next_index = self.index + 1
        return self.source[next_index] if next_index < len(self.source) else "\0"

    def _advance(self) -> str:
        ch = self.source[self.index]
        self.index += 1
        if ch == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return ch

    def _location(self) -> SourceLocation:
        return SourceLocation(self.index, self.line, self.column)

    def _at_end(self) -> bool:
        return self.index >= len(self.source)
