from __future__ import annotations

import argparse
import os
import sys
import tempfile
from collections.abc import Sequence
from pathlib import Path

from .compiler import compile_c_source
from .diagnostics import CompileError


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Compile a minimal C subset to NASM x86-64 Linux assembly."
    )
    parser.add_argument("source", type=Path, help="input C source file")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="write assembly to this file instead of stdout",
    )
    return parser


def atomic_write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temp_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=path.parent,
        text=True,
    )
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
    except BaseException:
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass
        raise


def main(argv: Sequence[str] | None = None) -> int:
    args = build_argument_parser().parse_args(argv)
    source_path: Path = args.source

    try:
        source = source_path.read_text(encoding="utf-8")
        assembly = compile_c_source(source)
        if args.output is None:
            sys.stdout.write(assembly)
        else:
            atomic_write_text(args.output, assembly)
        return 0
    except CompileError as error:
        print(
            error.render(source if "source" in locals() else "", str(source_path)),
            file=sys.stderr,
        )
        return 1
    except OSError as error:
        print(f"{source_path}: I/O error: {error}", file=sys.stderr)
        return 2
