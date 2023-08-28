import unittest
from core import *
from .linter_test import *
from core.rules import DuplicatedSetupRule
from core.rule import *


class ExtractSetupRewritter(LinterTest):

    def test_assert_true1(self):
        result = analyze(DuplicatedSetupRule,
                         """
class TestX(TestCase):
    def test_x(self):
        x = 2
        y = 2
        self.assertEquals(x,y)
    def test_y(self):
        x = 2
        y = 2
        self.assertEquals(y,x)""")
        expectedWarnings = [Warning('DuplicatedSetup', 2, 'there are 2 duplicated setup statements')]
        self.asssertWarning(result, expectedWarnings)

    def test_assert_true2(self):
        result = analyze(DuplicatedSetupRule,
                         """
class TestX(TestCase):
    def test_x(self):
        x = 2
        y = 2
        z = 5
        self.assertEquals(x,y)
    def test_y(self):
        x = 2
        g = 2
        z = 5
        f = 5
        self.assertEquals(y,x)""")
        expectedWarnings = [Warning('DuplicatedSetup', 1, 'there are 1 duplicated setup statements')]
        self.asssertWarning(result, expectedWarnings)

    def test_assert_true3(self):
        result = analyze(DuplicatedSetupRule,
                         """
class TestX(TestCase):
    def test_x(self):
        x = 1
        y = 2
        z = 5
        self.assertEquals(x,y)
    def test_y(self):
        x = 2
        g = 2
        z = 5
        f = 5
        self.assertEquals(y,x)""")
        expectedWarnings = []
        self.asssertWarning(result, expectedWarnings)

    def test_assert_true4(self):
        result = analyze(DuplicatedSetupRule,
                         """
class TestX(TestCase):
    def test_x(self):
        x = 5
        g = 3
        z = 1
        f = "a"
        self.assertEquals(z,f)
    def test_y(self):
        x = 5
        g = 3
        z = 1
        f = "a"
        self.assertEquals(z,f)""")
        expectedWarnings = [Warning('DuplicatedSetup', 5, 'there are 5 duplicated setup statements')]
        self.asssertWarning(result, expectedWarnings)

    def test_assert_true5(self):
        result = analyze(DuplicatedSetupRule,
                         """
class TestX(TestCase):
    def test_x(self):
        x = 5
        g = 3
        self.assertEquals(x,5)
    def test_y(self):
        x = 5
        g = 3
        self.assertEquals(g,3)
    def test_z(self):
        x = 5
        g = 3
        f = "a"
        self.assertEquals(x+g,8)""")
        expectedWarnings = [Warning('DuplicatedSetup', 2, 'there are 2 duplicated setup statements')]
        self.asssertWarning(result, expectedWarnings)

    def test_assert_true6(self):
        result = analyze(DuplicatedSetupRule,
                         """
class TestX(TestCase):
    def test_x(self):
        y = 5
        h = 3
        self.assertEquals(y,5)
    def test_y(self):
        x = 5
        g = 3
        self.assertEquals(g,3)
    def test_z(self):
        x = 5
        g = 3
        f = "a"
        self.assertEquals(x+g,8)""")
        expectedWarnings = []  # test_x es distinto al resto
        self.asssertWarning(result, expectedWarnings)


if __name__ == '__main__':
    unittest.main()
