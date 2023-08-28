import unittest
from core import *
from .linter_test import *
from core.rules import UncoupledMethodRule
from core.rule import *


class TestNoEvalRule(LinterTest):

    def test_eval_used(self):
        result = analyze(UncoupledMethodRule,
                         """class Demo:
                            def __init__(self):
                                self.x = 2
                                self.y = 3
                            def foo(self):
                                return self.x + self.y
                            def bar(self):
                                print("hola")
                            def zoo(self):
                                print(self.x)
                                """)
        expectedWarnings = [Warning('UncoupledMethodWarning', 7, 'method bar does not use any attribute')]
        self.asssertWarning(result, expectedWarnings)


if __name__ == '__main__':
    unittest.main()
