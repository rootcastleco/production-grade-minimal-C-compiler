from __future__ import annotations

from collections.abc import Sequence

from .ast_nodes import BinaryExpr, Expression, FunctionDefinition, NumberExpr, Program, ReturnStatement, UnaryExpr
from .diagnostics import ParseError, SourceSpan
from .tokens import Token, TokenKind


class Parser:
    def __init__(self, tokens: Sequence[Token]) -> None:
        self.tokens = tokens
        self.position = 0

    def parse_program(self) -> Program:
        function = self._parse_function()
        eof = self._consume(TokenKind.EOF, "expected end of file")
        return Program(function, SourceSpan(function.span.start, eof.span.end))

    def _parse_function(self) -> FunctionDefinition:
        start = self._consume(TokenKind.KW_INT, "expected 'int'")
        self._consume(TokenKind.KW_MAIN, "expected 'main'")
        self._consume(TokenKind.LPAREN, "expected '('")
        self._consume(TokenKind.RPAREN, "expected ')'")
        self._consume(TokenKind.LBRACE, "expected '{'")
        body = self._parse_statement()
        end = self._consume(TokenKind.RBRACE, "expected '}'")
        return FunctionDefinition("main", body, SourceSpan(start.span.start, end.span.end))

    def _parse_statement(self) -> ReturnStatement:
        start = self._consume(TokenKind.KW_RETURN, "expected 'return'")
        expression = self._parse_expression()
        end = self._consume(TokenKind.SEMICOLON, "expected ';' after return expression")
        return ReturnStatement(expression, SourceSpan(start.span.start, end.span.end))

    def _parse_expression(self) -> Expression:
        return self._parse_additive()

    def _parse_additive(self) -> Expression:
        expression = self._parse_multiplicative()
        while self._check(TokenKind.PLUS, TokenKind.MINUS):
            operator = self._advance()
            right = self._parse_multiplicative()
            expression = BinaryExpr(operator.kind, expression, right, SourceSpan(expression.span.start, right.span.end))
        return expression

    def _parse_multiplicative(self) -> Expression:
        expression = self._parse_unary()
        while self._check(TokenKind.STAR, TokenKind.SLASH):
            operator = self._advance()
            right = self._parse_unary()
            expression = BinaryExpr(operator.kind, expression, right, SourceSpan(expression.span.start, right.span.end))
        return expression

    def _parse_unary(self) -> Expression:
        if self._check(TokenKind.PLUS, TokenKind.MINUS):
            operator = self._advance()
            operand = self._parse_unary()
            return UnaryExpr(operator.kind, operand, SourceSpan(operator.span.start, operand.span.end))
        return self._parse_primary()

    def _parse_primary(self) -> Expression:
        if self._check(TokenKind.INTEGER):
            token = self._advance()
            assert token.integer_value is not None
            return NumberExpr(token.integer_value, token.span)
        if self._check(TokenKind.LPAREN):
            self._advance()
            expression = self._parse_expression()
            self._consume(TokenKind.RPAREN, "expected ')' after expression")
            return expression

        token = self._peek()
        description = "end of file" if token.kind is TokenKind.EOF else repr(token.lexeme)
        raise ParseError(f"expected integer or parenthesized expression, found {description}", token.span)

    def _consume(self, expected: TokenKind, message: str) -> Token:
        if self._check(expected):
            return self._advance()
        raise ParseError(message, self._peek().span)

    def _check(self, *kinds: TokenKind) -> bool:
        return self._peek().kind in kinds

    def _advance(self) -> Token:
        token = self._peek()
        if token.kind is not TokenKind.EOF:
            self.position += 1
        return token

    def _peek(self) -> Token:
        return self.tokens[self.position]
