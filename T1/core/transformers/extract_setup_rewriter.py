from ast import *
import ast
from core.rewriter import RewriterCommand
import inspect

class DuplicatedSetupVisitor(NodeVisitor):
    #  Implementar Clase
    def __init__(self):
        super().__init__()
        self.funct = []
        self.dict_functions = dict()
        self.contador_lineas = 0

    def visit_ClassDef(self, node):
        self.generic_visit(node)
        cantidad_funciones = len(self.funct)
        for i in self.funct:
            lista = []
            for j in i.body:
                lista.append(ast.dump(j))
            self.dict_functions[i.name] = lista
        cantidad_lineas = len(self.dict_functions[self.funct[0].name])
        #Hacemos un diccionario para cada una de las lineas 
        diccionario_lineas = dict()
        for i in range(cantidad_lineas):
            diccionario_lineas[i+1] = []
        keys = list(self.dict_functions.keys())
        for i in range(cantidad_lineas):
            for j in range(len(keys)):
                diccionario_lineas[i+1].append(self.dict_functions[keys[j]][i])
        contador_lineas = 0
        seguidos = True
        for key in diccionario_lineas:
            if diccionario_lineas[key].count(diccionario_lineas[key][0]) == cantidad_funciones and seguidos == True:
                contador_lineas += 1
            else: 
                seguidos = False
        self.contador_lineas = contador_lineas

    def visit_FunctionDef(self, node):
        self.funct.append(node)
        self.generic_visit(node)


class ExtractSetupTransformer(NodeTransformer):
    def __init__(self, lineas_iguales):
        super().__init__()
        self.funct = []
        self.variables_to_extract = dict()
        self.lineas_iguales = lineas_iguales
        self.funct_new_body = dict()

    def visit_FunctionDef(self, node):
        for i in range(self.lineas_iguales):
            # Necesito sacar el nombre de la variable en un Assign
            if isinstance(node.body[i], ast.Assign):
                for target in node.body[i].targets:
                    if isinstance(target, ast.Name):
                        self.variables_to_extract[target.id] = node.body[i]
        new_body = []
        for i in range(self.lineas_iguales, len(node.body)):
            new_body.append(node.body[i])
        self.funct_new_body[node.name] = new_body
        self.funct.append(node)
        self.generic_visit(node)
    
    def visit_ClassDef(self, node):
        self.generic_visit(node)
        # Debo crear una function def setUp(self) que contenga las lineas que se repiten y reemplazarlas por self.variable
        setup_func = FunctionDef(name="setUp", args=arguments(args=[arg(arg="self", annotation=None)], posonlyargs=[], kwonlyargs=[], kw_defaults=[], defaults=[]), body=[], decorator_list=[], returns=None)
        print(self.variables_to_extract)
        # Agregar asignaciones de variables a la función setUp
        for name, variable in self.variables_to_extract.items():
            if isinstance(variable, ast.Assign):
                for target in variable.targets:
                    if isinstance(target, ast.Attribute):
                        assign_node = Assign(
                            targets=[Attribute(value=Name(id="self", ctx=Load()), attr=target.attr, ctx=Store())],
                            value=variable.value
                        )
                        setup_func.body.append(assign_node)
        node.body.insert(0, setup_func)
        # Agregar el resto de las funciones al cuerpo de la clase
        for func_name, func_body in self.funct_new_body.items():
            function = FunctionDef(name=func_name, args=arguments(args=[arg(arg="self", annotation=None)], posonlyargs=[], kwonlyargs=[], kw_defaults=[], defaults=[]), body=func_body, decorator_list=[], returns=None)
            node.body.append(function)
        return node

    def visit_Name(self, node):
        self.generic_visit(node)
        current_function = inspect.currentframe().f_back.f_code.co_name
        if current_function != 'setUp' and node.id in self.variables_to_extract.keys():
            return Attribute(value=Name(id="self", ctx=Load()), attr=node.id, ctx=Load())
        return node


class ExtractSetupCommand(RewriterCommand):
    # Implementar comando, recuerde que puede necesitar implementar además clases NodeTransformer y/o NodeVisitor.
    def apply(self, node):
        visitor = DuplicatedSetupVisitor()
        visitor.visit(node)
        lineas_iguales = visitor.contador_lineas
        if lineas_iguales > 0:
            new_tree = fix_missing_locations(ExtractSetupTransformer(lineas_iguales).visit(node))
            return new_tree
        else:
            return node

    @classmethod
    def name(cls):
        return 'extract-setup'
