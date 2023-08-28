import ast
from ..rule import *


class DuplicatedSetupVisitor(NodeVisitor):
    #  Implementar Clase
    def __init__(self):
        pass


class DuplicatedSetupRule(Rule):
    #  Implementar Clase
    def analyze(self, node):
        pass

    @classmethod
    def name(cls):
        return 'duplicate-setup'
