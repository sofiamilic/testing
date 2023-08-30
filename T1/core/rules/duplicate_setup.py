from ..rule import *
from ast import *
import ast


class DuplicatedSetupVisitor(WarningNodeVisitor):
    #  Implementar Clase
    def __init__(self):
        super().__init__()
        self.funct = []
        self.dict_functions = dict()
        pass

    def visit_ClassDef(self, node):
        self.generic_visit(node)
        #print(self.funct)
        cantidad_funciones = len(self.funct)
        #print("Cantidad de funciones", cantidad_funciones)
        for i in self.funct:
            #print(i.body)
            lista = []
            for j in i.body:
                lista.append(ast.dump(j))
            self.dict_functions[i.name] = lista
        #print(self.dict_functions)
        cantidad_lineas = len(self.dict_functions[self.funct[0].name])
        #print("Cantidad de lineas", cantidad_lineas)
        #Hacemos un diccionario para cada una de las lineas 
        diccionario_lineas = dict()
        for i in range(cantidad_lineas):
            diccionario_lineas[i+1] = []
        #print(self.dict_functions)
        #print(diccionario_lineas) ## {1: [], 2: [], 3: []}
        keys = list(self.dict_functions.keys())
        #print(keys) ## ['test_x', 'test_y', 'test_z']
        for i in range(cantidad_lineas):
            for j in range(len(keys)):
                diccionario_lineas[i+1].append(self.dict_functions[keys[j]][i])
        #print(diccionario_lineas)
        contador_lineas = 0
        seguidos = True
        for key in diccionario_lineas:
            if diccionario_lineas[key].count(diccionario_lineas[key][0]) == cantidad_funciones and seguidos == True:
                contador_lineas += 1
            else: 
                seguidos = False
        if contador_lineas > 0:
            self.addWarning("DuplicatedSetup", contador_lineas, "there are "+ str(contador_lineas) + " duplicated setup statements")
        #print("Cantidad de lineas seguidas", contador_lineas)
        


    def visit_FunctionDef(self, node):
        self.funct.append(node)
        self.generic_visit(node)



class DuplicatedSetupRule(Rule):
    #  Implementar Clase
    def analyze(self, node):
        visitor = DuplicatedSetupVisitor()
        visitor.visit(node)
        #print(ast.dump(node, indent=2))
        return visitor.warningsList()
        

    @classmethod
    def name(cls):
        return 'duplicate-setup'

