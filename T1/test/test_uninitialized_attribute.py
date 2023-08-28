import unittest
from core import *
from .linter_test import *
from core.rules import UninitializedAttributeRule
from core.rule import *


class TestNoEvalRule(LinterTest):

    def test_eval_used(self):
        result = analyze(UninitializedAttributeRule,
                         """class Demo:
                            def __init__(self):
                                self.x = 2
                                self.y = 3
                            def foo(self):
                                return self.x + self.y
                            def bar(self):
                                print("hola")
                            def zoo(self):
                                print(self.z)
                                """)
        expectedWarnings = [Warning('UninitilizeAttrWarning', 10, 'attribute z was not initialized')]
        self.asssertWarning(result, expectedWarnings)


if __name__ == '__main__':
    unittest.main()
