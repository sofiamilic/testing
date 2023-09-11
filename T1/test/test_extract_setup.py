import unittest
from core import *
from core.rewriter import rewrite
from .linter_test import *
from core.transformers import *


class TestAssertTrueRule(LinterTest):

    def test_extract_setup(self):
        result = rewrite(ExtractSetupCommand,
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

        code = """
class TestX(TestCase):
    def setUp(self):
        self.x = 2
        self.y = 2
    def test_x(self):
        self.assertEquals(self.x,self.y)
    def test_y(self):
        self.assertEquals(self.y,self.x)"""

        self.assertAST(result,
                       """
class TestX(TestCase):
    def setUp(self):
        self.x = 2
        self.y = 2
    def test_x(self):
        self.assertEquals(self.x,self.y)
    def test_y(self):
        self.assertEquals(self.y,self.x)""")

    def test_extract_setup2(self):
        result = rewrite(ExtractSetupCommand,
                         """
class TestX(TestCase):
    def test_x(self):
        p = Person("Juan", "?")
        self.assertEquals(p.age(),3)
    def test_y(self):
        p = Person("Juan", "?")
        self.assertEquals(p.name(),"Juan")""")
        self.assertAST(result,
                       """class TestX(TestCase):
    def setUp(self):
        self.p = Person("Juan", "?")
    def test_x(self):
        self.assertEquals(self.p.age(),3)
    def test_y(self):
        self.assertEquals(self.p.name(),"Juan")""")

    def test_extract_setup_no_change(self):
        result = rewrite(ExtractSetupCommand,
                         """
class TestX(TestCase):
    def test_x(self):
        p = Person("Juan", "?")
        self.assertEquals(p.age(),3)
    def test_y(self):
        p = Person("Maria", "21")
        self.assertEquals(p.name(),"Maria")""")
        self.assertAST(result,
                       """
class TestX(TestCase):
    def test_x(self):
        p = Person("Juan", "?")
        self.assertEquals(p.age(),3)
    def test_y(self):
        p = Person("Maria", "21")
        self.assertEquals(p.name(),"Maria")""")

    def test_extract_setup_no_change2(self):
        result = rewrite(ExtractSetupCommand,
                         """
class TestX(TestCase):
    def test_x(self):
        p = Person("Juan", "?")
        self.assertEquals(p.age(),3)
    def test_y(self):
        p = Person("Juan", "?")
        self.assertEquals(p.name(),"Juan")
    def test_z(self):
        p = Person("Maria", "21")
        self.assertEquals(p.name(),"Maria")""")
        self.assertAST(result,
                       """
class TestX(TestCase):
    def test_x(self):
        p = Person("Juan", "?")
        self.assertEquals(p.age(),3)
    def test_y(self):
        p = Person("Juan", "?")
        self.assertEquals(p.name(),"Juan")
    def test_z(self):
        p = Person("Maria", "21")
        self.assertEquals(p.name(),"Maria")""")


    def test_extract_setup_3(self):
        result = rewrite(ExtractSetupCommand,
                         """
class TestX(TestCase):
    def test_x(self):
        x = 2
        for i in range(10):
            x = x + 1
        self.assertEquals(x,12)
    def test_y(self):
        x = 2
        for i in range(10):
            x = x + 1
        self.assertEquals(12,x)""")

        code = """
class TestX(TestCase):
    def setUp(self):
        self.x = 2
        for i in range(10):
            self.x = self.x + 1
    def test_x(self):
        self.assertEquals(self.x,12)
    def test_y(self):
        self.assertEquals(12,self.x)"""

        print(result)
        self.assertAST(result,code)

    def test_extract_setup_4(self):
        result = rewrite(ExtractSetupCommand,
                         """
class TestX(TestCase):
    def test_x(self):
        x = Person("Juan", "?")
        x.age = 2
        self.assertEquals(x.age,12)
    def test_y(self):
        x = Person("Juan", "?")
        x.age = 2
        self.assertEquals(12,x.age)""")

        code = """
class TestX(TestCase):
    def setUp(self):
        self.x = Person("Juan", "?")
        self.x.age = 2
    def test_x(self):
        self.assertEquals(self.x.age,12)
    def test_y(self):
        self.assertEquals(12,self.x.age)"""

        print(result)
        self.assertAST(result,code)

    def test_extract_setup_3(self):
        result = rewrite(ExtractSetupCommand,
                         """
class TestX(TestCase):
    def test_x(self):
        x = 2
        for i in range(10):
            x = x + 1
        self.assertEquals(x,12)
    def test_y(self):
        x = 2
        for i in range(10):
            x = x + 1
        self.assertEquals(12,x)""")

        code = """
class TestX(TestCase):
    def setUp(self):
        self.x = 2
        for i in range(10):
            self.x = self.x + 1
    def test_x(self):
        self.assertEquals(self.x,12)
    def test_y(self):
        self.assertEquals(12,self.x)"""

        print(result)
        self.assertAST(result,code)

    def test_extract_setup_5(self):
        result = rewrite(ExtractSetupCommand,
                         """
class TestX(TestCase):
    def test_x(self):
        x = Person("Juan", "?")
        create_person(x,2)
        self.assertEquals(x.age,12)
    def test_y(self):
        x = Person("Juan", "?")
        create_person(x,2)
        self.assertEquals(12,x.age)""")

        code = """
class TestX(TestCase):
    def setUp(self):
        self.x = Person("Juan", "?")
        create_person(self.x,2)
    def test_x(self):
        self.assertEquals(self.x.age,12)
    def test_y(self):
        self.assertEquals(12,self.x.age)"""

        print(result)
        self.assertAST(result,code)

if __name__ == '__main__':
    unittest.main()
