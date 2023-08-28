import unittest
from core import *
from core.rewriter import rewrite
from .linter_test import *
from core.transformers import *


class TestNoEvalRule(LinterTest):
    def test_eval_used(self):
        result = rewrite(IfTrueRewriterCommand,
                         """
if True :
    return x
else :
    return y
    """)
        self.assertAST(result, "return x")


if __name__ == '__main__':
    unittest.main()
