import importlib.util
import unittest
import sys
from pathlib import Path

MODULE_PATH = Path(__file__).with_name("minimal_c_compiler_pg.py")
spec = importlib.util.spec_from_file_location("minimal_c_compiler_pg", MODULE_PATH)
assert spec is not None and spec.loader is not None
compiler = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = compiler
spec.loader.exec_module(compiler)


class CompilerTests(unittest.TestCase):
    def test_operator_precedence(self):
        assembly = compiler.compile_c_source("int main() { return 2 + 3 * 4; }")
        self.assertIn("imul eax, ecx", assembly)
        self.assertIn("add eax, ecx", assembly)
        self.assertLess(assembly.index("imul eax, ecx"), assembly.index("add eax, ecx"))

    def test_parentheses(self):
        assembly = compiler.compile_c_source("int main() { return (2 + 3) * 4; }")
        self.assertLess(assembly.index("add eax, ecx"), assembly.index("imul eax, ecx"))

    def test_comments_and_unary_plus_minus(self):
        assembly = compiler.compile_c_source(
            "int main() { /* block */ return -(+7); // line\n }"
        )
        self.assertIn("mov eax, 7", assembly)
        self.assertIn("neg eax", assembly)

    def test_int32_min(self):
        assembly = compiler.compile_c_source("int main() { return -2147483648; }")
        self.assertIn("mov eax, 0x80000000", assembly)

    def test_positive_literal_overflow(self):
        with self.assertRaises(compiler.CompileError):
            compiler.compile_c_source("int main() { return 2147483648; }")

    def test_constant_division_by_zero(self):
        with self.assertRaisesRegex(compiler.CompileError, "division by zero"):
            compiler.compile_c_source("int main() { return 10 / (3 - 3); }")

    def test_unknown_identifier_has_location(self):
        source = "int main() { return value; }"
        with self.assertRaises(compiler.LexError) as context:
            compiler.compile_c_source(source)
        rendered = context.exception.render(source, "test.c")
        self.assertIn("test.c:1:21", rendered)
        self.assertIn("unknown identifier", rendered)

    def test_missing_semicolon(self):
        with self.assertRaises(compiler.ParseError):
            compiler.compile_c_source("int main() { return 42 }")

    def test_codegen_uses_caller_saved_register(self):
        assembly = compiler.compile_c_source("int main() { return 8 / 2; }")
        self.assertIn("idiv ecx", assembly)
        self.assertNotIn("ebx", assembly)


if __name__ == "__main__":
    unittest.main()
