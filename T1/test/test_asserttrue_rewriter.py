import unittest
from core import *
from core.rewriter import rewrite
from .linter_test import *
from core.transformers import *


class TestAssertTrueRewritter(LinterTest):
    def test_eval_used(self):
        result = rewrite(AssertTrueCommand, "self.assertEquals(x, True)")
        self.assertAST(result, "self.assertTrue(x)")

    def test_eval_used2(self):
        result = rewrite(AssertTrueCommand, """
def test_x(self):
    self.assertEquals(x, True)
    self.assertEquals(y, True)""")
        self.assertAST(result, """
def test_x(self):
    self.assertTrue(x)
    self.assertTrue(y)""")

    def test_eval_used_no_change(self):
        result = rewrite(AssertTrueCommand, """
def test_x(self):
    self.assertTrue(x)""")
        self.assertAST(result, """
def test_x(self):
    self.assertTrue(x)""")

    def test_eval_used_mix(self):
        result = rewrite(AssertTrueCommand, """
def test_x(self):
    self.assertTrue(x)
        
def test_y(self):
    self.assertEquals(y, True)""")

        self.assertAST(result, """
def test_x(self):
    self.assertTrue(x)
        
def test_y(self):
    self.assertTrue(y)""")


if __name__ == '__main__':
    unittest.main()
