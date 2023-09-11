import unittest
from core import *
from .linter_test import *
from core.rules import UnusedVariableTestRule
from core.rule import *


class TestUnusedVariable(LinterTest):

    def test_unused_variable(self):
        result = analyze(UnusedVariableTestRule,
                         """def test_x(self):
                            x = 2
                            y = 2
                            z = False
                            self.assertTrue(z)""")

        expectedWarnings = [Warning('UnusedVariable', 2, 'variable x has not been used'),
                            Warning('UnusedVariable', 3, 'variable y has not been used')]

        self.asssertWarning(result, expectedWarnings)

    def test_unused_variable2(self):
        result = analyze(UnusedVariableTestRule,
                         """def test_x(self):
                            x = 2
                            y = x + 2
                            z = False
                            self.assertTrue(z)""")
        expectedWarnings = [Warning('UnusedVariable', 3, 'variable y has not been used')]

        self.asssertWarning(result, expectedWarnings)

    def test_unused_variable3(self):
        result = analyze(UnusedVariableTestRule,
                         """def test_x(self):
                            x = 2 
                            self.assertTrue(x)""")
        expectedWarnings = []
        self.asssertWarning(result, expectedWarnings)

    def test_unused_variable4(self):
        result = analyze(UnusedVariableTestRule,
                         """class TestCase():
    def test_x(self):
        x = 2
        y = 2
        z = False
        self.assertTrue(z)

    def test_y(self):
        x = 2
        y = x + 2
        z = False
        self.assertTrue(z)""")
        expectedWarnings = [Warning('UnusedVariable', 3, 'variable x has not been used'),
                            Warning('UnusedVariable', 4, 'variable y has not been used'),
                            Warning('UnusedVariable', 10, 'variable y has not been used')]
        print(result)
        self.asssertWarning(result, expectedWarnings)
    
    def test_unused_variable5(self):
        result = analyze(UnusedVariableTestRule,
                         """class TestCase():
    def test_x(self):
        x = 2
        y = 2 * x
        z = False
        self.assertTrue(z)

    def test_y(self):
        x = 2
        p = Person("Juan", "?")
        z = False
        self.assertTrue(z)""")
        expectedWarnings = [Warning('UnusedVariable', 4, 'variable y has not been used'),
                            Warning('UnusedVariable', 9, 'variable x has not been used'),
                            Warning('UnusedVariable', 10, 'variable p has not been used')]
        print(result)
        self.asssertWarning(result, expectedWarnings)


if __name__ == '__main__':
    unittest.main()
