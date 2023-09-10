import unittest
from core import *
from .linter_test import *
from core.rules import AssertionLessTestRule
from core.rule import *
from os.path import join


class TestNoEvalRule(LinterTest):

    def test_with_assertion(self):
        result = analyze(AssertionLessTestRule,
                         """def test_x(self):
                            x = 2
                            y = 3
                            self.assertEquals(2,3)""")
        expectedWarnings = []
        self.asssertWarning(result, expectedWarnings)

    def test_without_assertion(self):
        result = analyze(AssertionLessTestRule,
                         """def test_x(self):
                            x = 2
                            y = 3""")
        expectedWarnings = [Warning('AssertionLessWarning', 1, 'it is an assertion less test')]
        self.asssertWarning(result, expectedWarnings)

    def test_without_multiple_assertion(self):
        result = analyze(AssertionLessTestRule,
                         """class TestCase():
    def test_x(self):
        x = 2

    def test_y(self):
        y = 5
        """)
        expectedWarnings = [Warning('AssertionLessWarning', 2, 'it is an assertion less test'),
                            Warning('AssertionLessWarning', 5, 'it is an assertion less test')]
        self.asssertWarning(result, expectedWarnings)

    def test_assert_string(self):
        result = analyze(AssertionLessTestRule,
                         """class TestCase():
    def test_x(self):
        x = 2
        y = "assert"

    def test_y(self):
        y = 5
        """)
        expectedWarnings = [Warning('AssertionLessWarning', 2, 'it is an assertion less test'),
                            Warning('AssertionLessWarning', 6, 'it is an assertion less test')]
        self.asssertWarning(result, expectedWarnings)


if __name__ == '__main__':
    unittest.main()
