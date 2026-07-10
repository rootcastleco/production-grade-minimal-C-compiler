#!/usr/bin/env python3
"""Compatibility entrypoint for the production-grade minimal C compiler."""

from minimal_c_compiler import (
    CodegenError,
    CompileError,
    LexError,
    ParseError,
    compile_c_source,
)
from minimal_c_compiler.cli import main

__all__ = [
    "CodegenError",
    "CompileError",
    "LexError",
    "ParseError",
    "compile_c_source",
    "main",
]


if __name__ == "__main__":
    raise SystemExit(main())
