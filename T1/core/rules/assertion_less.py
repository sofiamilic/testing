from ..rule import *


class AssertionLessVisitor(WarningNodeVisitor):
    # Implementar Clase
    def __init__(self):
        pass


class AssertionLessTestRule(Rule):
    #  Implementar Clase
    def analyze(self, node):
        pass

        
    @classmethod
    def name(cls):
        return 'assertion-less'
