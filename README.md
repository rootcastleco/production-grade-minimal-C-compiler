# Minimal C Compiler PG

A small, testable compiler for a deliberately limited C subset:

```c
int main() {
    return <expression>;
}
```

It emits NASM-compatible x86-64 Linux assembly.

## Supported expressions

- Decimal 32-bit integer literals
- Parentheses
- Unary `+` and `-`
- Binary `+`, `-`, `*`, `/`
- C-style line and block comments

## Requirements

- Python 3.10+
- NASM
- GNU `ld`
- x86-64 Linux for generated executables

## Compile

```bash
python3 minimal_c_compiler_pg.py sample.c -o sample.s
nasm -f elf64 sample.s -o sample.o
ld sample.o -o sample
./sample
echo $?
```

Without `-o`, assembly is written to standard output:

```bash
python3 minimal_c_compiler_pg.py sample.c > sample.s
```

## Tests

```bash
python3 -m unittest -v test_minimal_c_compiler_pg.py
```

## Scope

This is an educational compiler, not a complete C implementation. It intentionally excludes variables, function parameters, control flow, comparisons, pointers, and the standard library.
