from ..rule import *


class UnusedVariableVisitor(WarningNodeVisitor):
    #  Implementar Clase
    def __init__(self):
        super().__init__()
        self.variables = dict()
        pass

    def visit_FunctionDef(self, node):
        #print("Estoy entrando a una funcion")
        self.func_variables = dict()
        self.generic_visit(node)
        #print("Variables de la funcion", self.func_variables)
        for key in self.func_variables:
            self.addWarning("UnusedVariable", self.func_variables[key].lineno, "variable " + key + " has not been used")

        
    def visit_Assign(self, node):
        #print("Linea", node.lineno)
        for target in node.targets:
            #print("Target", target.id)
            self.func_variables[target.id] = node.value
        self.generic_visit(node)
    
    def visit_Call(self, node):
        #print("Estoy entrando a un assert")
        for arg in node.args:
            if isinstance(arg, Name):
                #print("Argumento", arg.id)
                if arg.id in self.func_variables:
                    del self.func_variables[arg.id]
    
    def visit_BinOp(self,node):
        #print("Estoy entrando a un binop")
        if isinstance(node.left, Name):
            if node.left.id in self.func_variables:
                del self.func_variables[node.left.id]
        if isinstance(node.right, Name):
            if node.right.id in self.func_variables:
                del self.func_variables[node.right.id]
        

class UnusedVariableTestRule(Rule):
    #  Implementar Clase
    def analyze(self, node):
        visitor = UnusedVariableVisitor()
        visitor.visit(node)
        return visitor.warningsList()
        pass
        
    @classmethod
    def name(cls):
        return 'not-used-variable'
