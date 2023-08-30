from ..rule import *


class AssertionLessVisitor(WarningNodeVisitor):
    # Implementar Clase
    def __init__(self):
        super().__init__()

    def visit_FunctionDef(self, node):
        code = dump(node)
        if "assert" not in code:
            self.addWarning("AssertionLessWarning", node.lineno, "it is an assertion less test")
        self.generic_visit(node)


class AssertionLessTestRule(Rule):
    #  Implementar Clase
    def analyze(self, node):
        visitor = AssertionLessVisitor()
        visitor.visit(node)
        return visitor.warningsList()

        
    @classmethod
    def name(cls):
        return 'assertion-less'
