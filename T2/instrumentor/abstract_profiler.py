from function_instrumentor import *
import threading


# Clase que representa la estructura de un profiler
class AbstractProfiler:
    __singleton_lock = threading.Lock()
    __singleton_instance = None

    # Usamos un singleton para no crear instancias a cada rato
    @classmethod
    def getInstance(cls):
        with cls.__singleton_lock:
            if not cls.__singleton_instance:
                cls.__singleton_instance = cls()
        return cls.__singleton_instance

    # Al resetear actualizamos la instancia de singleton a None
    @classmethod
    def reset(cls):
        cls.__singleton_instance = None

    # Este metodo se llama cada vez se ejecuta una funcion
    @classmethod
    def record_start(cls, functionName, args):
        cls.getInstance().fun_call_start(functionName, args)

    @classmethod
    def record_end(cls, functionName, returnValue):
        cls.getInstance().fun_call_end(functionName, returnValue)
        return returnValue

    def fun_call_start(self, functionName, args):
        pass
    
    def fun_call_end(self, functionName, returnValue):
        pass

    def get_callers(self, code):
        pass
    
    # recibe un archivo que contiene un programa
    # lo instrumenta y lo ejecuta recolectando datos en el profiler
    # devuelve el objeto profiler con los datos
    @classmethod
    def profile(cls, fileName):
        cls.reset()
        instance = cls.getInstance()
        ast = cls.get_ast_from_file(fileName)
        newAst = cls.instrument(ast)
        #print("Aca estoy")
        print(unparse(newAst))  # Esta línea imprime el codigo modificado después de inyectarle líneas con el profiler pueden comentarla o descomentarla si quieren
        cls.getInstance().get_callers(unparse(newAst))
        exec(compile(newAst, filename="<ast>", mode ="exec"), locals(), locals())
        return instance
    
    # Este metodo injecta codigo al inicio de cada funcion en el programa
    @classmethod
    def instrument(cls, ast):
        visitor = FunctionInstrumentor()

# Marcar la función como no cacheable antes de la instrumentación
        if isinstance(ast, FunctionDef):
            functionName = ast.name
            cls.getInstance().set_function_uncacheable(functionName)

        # Agregar un nuevo nodo `return` al final de la función instrumentada
        if isinstance(ast, FunctionDef) and ast.body:
            last_statement = ast.body[-1]
            if not isinstance(last_statement, Return):
                return_value = Call(
                    func=Attribute(
                        value=Name(id='Profiler', ctx=Load()),
                        attr='record_end',
                        ctx=Load()
                    ),
                    args=[
                        Constant(value=functionName),
                        Name(id=last_statement.targets[0].id, ctx=Load()) if isinstance(last_statement, Assign) else last_statement.value
                    ],
                    keywords=[]
                )
                ast.body[-1] = Return(value=return_value)

        return fix_missing_locations(visitor.visit(ast))
    
    # recupera el AST dado un archivo
    @classmethod
    def get_ast_from_file(cls, fileName):
        file = open(fileName)
        fileContent = file.read()
        file.close()
        tree = parse(fileContent)
        return tree
    
    