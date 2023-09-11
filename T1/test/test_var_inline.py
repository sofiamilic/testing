import unittest
from core import *
from core.rewriter import rewrite
from .linter_test import *
from core.transformers import *


class TestInlineRewriter(LinterTest):
    def test_inline(self):
        result = rewrite(InlineCommand,
                         """def test(self):
                            x = 3
                            self.assertEquals(x,2)""")
        
        self.assertAST(result, """def test(self):
                        self.assertEquals(3,2)""")

    def test_inline2(self):
        result = rewrite(InlineCommand,
                         """def test(self):
                            x = complex_method()
                            self.assertEquals(x,2)""")
        
        self.assertAST(result, """def test(self):
                        self.assertEquals(complex_method(),2)""")

    def test_inline3(self):
        result = rewrite(InlineCommand,
                         """def test(self):
                            x = complex_method()
                            y = x + 2
                            self.assertEquals(y,2)""")
        
        self.assertAST(result, """def test(self):
                       self.assertEquals(complex_method() + 2,2)""")

    def test_inline4(self):
        result = rewrite(InlineCommand,
                         """def test(self):
                            x = complex_method()
                            y = x + 2
                            z = x + y
                            self.assertEquals(z,2)""")
        
        code = """def test(self):
                            x = complex_method()
                            self.assertEquals(x + (x + 2), 2)"""

        self.assertAST(result, """def test(self):
                            x = complex_method()
                            self.assertEquals(x + (x + 2), 2)""")

    def test_inline5(self):
        result = rewrite(InlineCommand,
                         """def test(self):
                            x = complex_method()
                            y = x + 2
                            z = x + y
                            h = z + y
                            self.assertEquals(h, 2)""")

        self.assertAST(result, """def test(self):
                            x = complex_method()
                            y = x + 2
                            self.assertEquals(x + y + y, 2)""")
    
    def test_inline6(self):
        result = rewrite(InlineCommand,
                         """def test(self):
                            x = complex_method()
                            y = x + 2
                            for i in range(10):
                                y = y + 1""")

        self.assertAST(result, """def test(self):
                            y = complex_method() + 2
                            for i in range(10):
                                y = y + 1""")


if __name__ == '__main__':
    unittest.main()
