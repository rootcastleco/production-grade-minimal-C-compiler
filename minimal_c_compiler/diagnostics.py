from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SourceLocation:
    offset: int
    line: int
    column: int


@dataclass(frozen=True, slots=True)
class SourceSpan:
    start: SourceLocation
    end: SourceLocation


class CompileError(Exception):
    """Base class for user-facing compile errors."""

    def __init__(self, message: str, span: SourceSpan | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.span = span

    def render(self, source: str, filename: str) -> str:
        if self.span is None:
            return f"{filename}: error: {self.message}"

        line_no = self.span.start.line
        column = self.span.start.column
        lines = source.splitlines()
        source_line = lines[line_no - 1] if 0 < line_no <= len(lines) else ""

        width = max(1, self.span.end.offset - self.span.start.offset)
        caret = " " * max(0, column - 1) + "^" * width
        return (
            f"{filename}:{line_no}:{column}: error: {self.message}\n"
            f"    {source_line}\n"
            f"    {caret}"
        )


class LexError(CompileError):
    pass


class ParseError(CompileError):
    pass


class CodegenError(CompileError):
    pass
