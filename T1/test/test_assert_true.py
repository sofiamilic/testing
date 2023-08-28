from .linter_test import *
from core.rules import AssertionTrueTestRule
from core.rule import *


class TestAssertTrueRule(LinterTest):

    def test_assert_true1(self):
        result = analyze(AssertionTrueTestRule,
                         """def test_x(self):
                            x = 2
                            self.assertTrue(True)""")
        expectedWarnings = [Warning('AssertTrueWarning', 3, 'useless assert true detected')]
        self.asssertWarning(result, expectedWarnings)

    def test_assert_true2(self):
        result = analyze(AssertionTrueTestRule,
                         """def test_x(self):
                            self.assertTrue(True)
                            x = 2
                            self.assertTrue(True)
                            print(x)""")
        expectedWarnings = [Warning('AssertTrueWarning', 2, 'useless assert true detected'),
                            Warning('AssertTrueWarning', 4, 'useless assert true detected')]
        self.asssertWarning(result, expectedWarnings)

    def test_assert_true_variable_True(self):
        result = analyze(AssertionTrueTestRule,
                         """def test_x(self):
                            x = True
                            self.assertTrue(x)""")
        expectedWarnings = [Warning('AssertTrueWarning', 3, 'useless assert true detected')]
        self.asssertWarning(result, expectedWarnings)

    def test_assert_true_no_warning(self):
        result = analyze(AssertionTrueTestRule,
                         """def test_x(self):
                            x = False
                            self.assertTrue(x)
                            self.assertTrue(False)""")
        expectedWarnings = []
        self.asssertWarning(result, expectedWarnings)

    def test_assert_true_no_warning2(self):
        result = analyze(AssertionTrueTestRule,
                         """def test_x(self):
                            x = 5
                            self.assertEqual(x, 5)""")
        expectedWarnings = []
        self.asssertWarning(result, expectedWarnings)

    def test_assert_true_mix(self):
        result = analyze(AssertionTrueTestRule,
                         """def test_x(self):
                            x = 9
                            y = True
                            self.assertTrue(True)
                            self.assertEqual(x, 9)
                            self.assertTrue(y)

                            """)
        expectedWarnings = [Warning('AssertTrueWarning', 4, 'useless assert true detected'),
                            Warning('AssertTrueWarning', 6, 'useless assert true detected')]
        self.asssertWarning(result, expectedWarnings)

    def test_assert_true_multiple_tests(self):
        result = analyze(AssertionTrueTestRule,
                         """class TestCase():
    def test_x(self):
        x = 2
        self.assertEqual(x, 2)
        self.assertTrue(True)

    def test_y(self):
        y = 5
        z = y + 2
        w = True
        self.assertTrue(w)
        self.assertTrue(True)
        self.assertEqual(z, 7)""")
        expectedWarnings = [Warning('AssertTrueWarning', 5, 'useless assert true detected'),
                            Warning('AssertTrueWarning', 11, 'useless assert true detected'),
                            Warning('AssertTrueWarning', 12, 'useless assert true detected')]
        self.asssertWarning(result, expectedWarnings)


if __name__ == '__main__':
    unittest.main()
