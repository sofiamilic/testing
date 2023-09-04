from ast import *
import ast
from core.rewriter import RewriterCommand

class AssertTrueTransformer(NodeTransformer):
    def visit_Call(self, node):
        #print(ast.dump(node, indent=4))
        # Cambiamos los self.assertEquals(x, True) por assertTrue(x)
        if isinstance(node.func, Attribute):
            if node.func.attr == 'assertEquals':
                if len(node.args) == 2 and isinstance(node.args[1], NameConstant) and node.args[1].value == True:
                    return Call(func=Attribute(value=node.func.value, attr='assertTrue', ctx=Load()), args=[node.args[0]], keywords=[])
            else:
                return Call(func=Attribute(value=node.func.value, attr=node.func.attr, ctx=Load()), args=node.args, keywords=node.keywords)
        self.generic_visit(node)

class AssertTrueCommand(RewriterCommand):
    # Implementar comando, recuerde que puede necesitar implementar además clases NodeTransformer y/o NodeVisitor.

    def apply(self, node):
        print(ast.dump(node, indent=4))
        new_tree = fix_missing_locations(AssertTrueTransformer().visit(node))
        return new_tree

