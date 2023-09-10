from ..rule import *


class AssertionLessVisitor(WarningNodeVisitor):
    # Implementar Clase
    def __init__(self):
        super().__init__()

    def visit_FunctionDef(self, node):
        is_assert = False
        for stmt in node.body:
            if isinstance(stmt, Expr):
                if isinstance(stmt.value, Call):
                    if isinstance(stmt.value.func, Attribute):
                        if "assert" in stmt.value.func.attr:
                            is_assert = True
        if not is_assert:
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
