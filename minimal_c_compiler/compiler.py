from __future__ import annotations

from .codegen import X86_64CodeGenerator
from .lexer import Lexer
from .parser import Parser
from .semantic import validate_program


def compile_c_source(source_code: str) -> str:
    tokens = Lexer(source_code).tokenize()
    program = Parser(tokens).parse_program()
    validate_program(program)
    return X86_64CodeGenerator().generate(program)
