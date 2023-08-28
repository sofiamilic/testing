from ..rule import *

class AssertionTrueVisitor(WarningNodeVisitor):
    #  Implementar Clase
    def __init__(self):
        pass
    

class AssertionTrueTestRule(Rule):
    #  Implementar Clase
    def analyze(self, node):
        pass
        
    @classmethod
    def name(cls):
        return 'assertion-true'
