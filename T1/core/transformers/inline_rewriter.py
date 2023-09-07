from ast import *
import ast
from core.rewriter import RewriterCommand
from collections import defaultdict
from copy import deepcopy

class VariableUsageCounter(NodeVisitor):
    def __init__(self):
        self.variable_assignments = defaultdict(int)
        self.variable_count = defaultdict(int)

    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name):
                variable_name = target.id
                self.variable_count[variable_name] += 1
                self.variable_assignments[variable_name] += 1
        self.generic_visit(node)

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load):
            if node.id in self.variable_assignments:
                self.variable_count[node.id] += 1
        self.generic_visit(node)

class InlineTransformer(NodeTransformer):
    def __init__(self, variables_used_once):
        super().__init__()
        self.variables_used_once = variables_used_once
        self.variables = {}
    
    def visit_Name(self, node):
        if isinstance(node, ast.Name) and node.id in self.variables:
            if node.id in self.variables_used_once:
                node = self.recursive_assign(self.variables[node.id])
                return node
        return self.generic_visit(node)
    
    def recursive_assign(self, node):
        if isinstance(node, Name) and node.id in self.variables_used_once:
            return self.variables[node.id]
        elif isinstance(node, ast.BinOp):
            node.left = self.recursive_assign(node.left)
            node.right = self.recursive_assign(node.right)
        elif isinstance(node, ast.UnaryOp):
            node.operand = self.recursive_assign(node.operand)
        elif isinstance(node, ast.Call):
            node.args = [self.recursive_assign(arg) for arg in node.args]
        return node

    def visit_Assign(self, node):
        if len(node.targets) == 1 and isinstance(node.targets[0], Name):
            variable_name = node.targets[0].id
            self.variables[variable_name] = deepcopy(node.value)
            if variable_name in self.variables_used_once:
                # No devolvemos nada para eliminar esta asignación
                return None
        return self.generic_visit(node)       

def find_variables_used_once(node):
    counter = VariableUsageCounter()
    counter.visit(node)
    variables_used_once = set()
    for variable, assignments in counter.variable_assignments.items():
        if assignments == 1 and counter.variable_count[variable] == 2:
            variables_used_once.add(variable)
    return variables_used_once

class InlineCommand(RewriterCommand):
    # Implementar comando, recuerde que puede necesitar implementar además clases NodeTransformer y/o NodeVisitor.
    
    def apply(self, node):
        # La funcion fix_missing_locations se utiliza para recorrer los nodos del AST y actualizar ciertos atributos
        # (e.g., número de línea) considerando ahora la modificacion
        variables_used_once = find_variables_used_once(node)
        new_tree = fix_missing_locations(InlineTransformer(variables_used_once).visit(node))
        return new_tree
