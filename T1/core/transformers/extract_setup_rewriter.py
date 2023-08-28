from ast import *
import ast
from core.rewriter import RewriterCommand



class ExtractSetupCommand(RewriterCommand):
    # Implementar comando, recuerde que puede necesitar implementar además clases NodeTransformer y/o NodeVisitor.
    def apply(self, node):
        pass

    @classmethod
    def name(cls):
        return 'extract-setup'
