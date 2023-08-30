from ..rule import *

class AssertionTrueVisitor(WarningNodeVisitor):
    #  Implementar Clase
    def __init__(self):
        super().__init__()
        self.true_variables = set()
        pass

    def visit_Assign(self, node):
        if (isinstance(node.value, NameConstant) and node.value.value == True):
            for target in node.targets:
                if (isinstance(target, Name)):
                    self.true_variables.add(target.id)
        self.generic_visit(node)

    def visit_Call(self, node):
        if (isinstance(node.func, Attribute) and isinstance(node.func.value, Name) and node.func.value.id == 'self' and node.func.attr == 'assertTrue'):
            funcArgs = node.args
            if (len(funcArgs) == 1 and isinstance(funcArgs[0], Name) and funcArgs[0].id in self.true_variables):
                self.addWarning("AssertTrueWarning", node.lineno, "useless assert true detected")
            elif (len(funcArgs) == 1 and isinstance(funcArgs[0], NameConstant) and funcArgs[0].value == True):
                self.addWarning("AssertTrueWarning", node.lineno, "useless assert true detected")

class AssertionTrueTestRule(Rule):
    #  Implementar Clase
    def analyze(self, node):
        visitor = AssertionTrueVisitor()
        visitor.visit(node)
        return visitor.warningsList()
        
    @classmethod
    def name(cls):
        return 'assertion-true'
