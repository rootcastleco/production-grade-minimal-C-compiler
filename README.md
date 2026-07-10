# Production-Grade Minimal C Compiler

[![Python](https://img.shields.io/badge/Python-3.10%2B-0E3D8A?logo=python&logoColor=white)](https://www.python.org/)
[![Target](https://img.shields.io/badge/Target-x86--64%20Linux-228B55?logo=linux&logoColor=white)](https://www.kernel.org/)
[![Assembly](https://img.shields.io/badge/Assembly-NASM-000000)](https://www.nasm.us/)
[![Rootcastle](https://img.shields.io/badge/Rootcastle-Engineering%20%26%20Innovation-0E3D8A)](https://www.rootcastle.com/)

A compact, testable compiler that translates a deliberately restricted subset of C into NASM-compatible x86-64 Linux assembly.

The project is designed as an educational compiler pipeline with production-oriented engineering practices: typed AST nodes, source-aware diagnostics, semantic validation, deterministic code generation, atomic output writes, modular architecture, and automated tests.

```c
int main() {
    return (7 + 5) * 3 / 2 - 4;
}
```

## Compiler pipeline

```text
C source
   |
   v
Lexer -> Token stream -> Recursive-descent parser -> Typed AST
   |                                             |
   +------ source spans and diagnostics --------+
                                                 |
                                                 v
                                  Semantic validation
                                                 |
                                                 v
                                  x86-64 NASM codegen
                                                 |
                                                 v
                                      Linux assembly
```

## Supported language subset

The accepted program structure is intentionally narrow:

```c
int main() {
    return <expression>;
}
```

Supported expression features:

- Signed decimal 32-bit integer literals
- Parenthesized expressions
- Unary `+` and `-`
- Binary `+`, `-`, `*`, and `/`
- Standard arithmetic precedence and left associativity
- `//` line comments
- `/* ... */` block comments

## Engineering features

- Modular lexer, parser, semantic-analysis, and code-generation stages
- Immutable `dataclass`-based AST and token models
- Line, column, and source-span-aware compiler diagnostics
- `INT32_MIN` handling and positive integer overflow checks
- Compile-time detection of constant division by zero
- Signed x86 division using `cdq` and `idiv`
- Caller-saved temporary registers in generated code
- Internal expression-stack balance validation
- Atomic file output to prevent partial assembly artifacts
- Stable Python API through `compile_c_source()`
- CLI exit codes for compile and I/O failures
- Unit tests covering precedence, comments, literals, diagnostics, and codegen

## Requirements

- Python 3.10 or newer
- NASM
- GNU `ld`
- x86-64 Linux for executing generated binaries

## Usage

Generate assembly:

```bash
python3 minimal_c_compiler_pg.py sample.c -o sample.s
```

Or write assembly to standard output:

```bash
python3 minimal_c_compiler_pg.py sample.c > sample.s
```

Assemble, link, and execute:

```bash
nasm -f elf64 sample.s -o sample.o
ld sample.o -o sample
./sample
echo $?
```

## Python API

```python
from minimal_c_compiler import compile_c_source

source = "int main() { return 6 * 7; }"
assembly = compile_c_source(source)
print(assembly)
```

## Diagnostics

Invalid programs produce location-aware errors:

```text
example.c:2:18: error: division by zero
    return 10 / (2 - 2);
                 ^^^^^
```

## Tests

Run the complete test suite:

```bash
python3 -m unittest -v test_minimal_c_compiler_pg.py
```

Current test coverage includes:

- Arithmetic precedence
- Parentheses
- Unary operators
- Comment handling
- `INT32_MIN`
- Literal overflow
- Constant division by zero
- Missing semicolons
- Source-location diagnostics
- ABI-conscious register selection

## Project structure

```text
.
├── minimal_c_compiler_pg.py       # Compatibility CLI entrypoint
├── minimal_c_compiler/
│   ├── __init__.py                # Public Python API
│   ├── ast_nodes.py               # Typed AST model
│   ├── cli.py                     # Command-line interface
│   ├── codegen.py                 # x86-64 NASM generator
│   ├── compiler.py                # Compilation pipeline
│   ├── diagnostics.py             # Source locations and errors
│   ├── lexer.py                   # Lexical analysis
│   ├── parser.py                  # Recursive-descent parser
│   ├── semantic.py                # Semantic validation
│   └── tokens.py                  # Token definitions
├── test_minimal_c_compiler_pg.py
├── sample.c
└── sample.s
```

## Scope and limitations

This repository is not a complete implementation of ISO C. It intentionally excludes:

- Variables and assignments
- Function parameters and multiple functions
- Conditions and loops
- Comparisons and logical operators
- Pointers, arrays, structs, and memory management
- Includes, macros, and preprocessing
- The standard library
- Full C integer-overflow semantics

`INT32_MIN / -1` may still raise a processor division-overflow exception at runtime because that quotient cannot be represented in a signed 32-bit register.

## Security model

The compiler does not execute source code during compilation. Input is parsed into a constrained AST and emitted as deterministic assembly. Nevertheless, generated binaries should be treated as untrusted artifacts and executed inside an isolated environment when source provenance is unknown.

## Suggested repository topics

`c-compiler` · `compiler-design` · `python` · `x86-64` · `nasm` · `assembly` · `lexer` · `parser` · `ast` · `recursive-descent-parser` · `systems-programming` · `education` · `rootcastle`

## Branding and authorship

Developed by **Batuhan Ayrıbaş** under **Rootcastle Engineering & Innovation**.

- Rootcastle Engineering & Innovation: [rootcastle.com](https://www.rootcastle.com/)
- Batuhan Ayrıbaş: [batuhanayribas.com](https://batuhanayribas.com/)
- GitHub: [@rootcastleco](https://github.com/rootcastleco)

---

**Rootcastle Engineering & Innovation**  
Engineering software, IoT systems, data infrastructure, and rapid hardware prototyping with an evidence-driven, test-first approach.
