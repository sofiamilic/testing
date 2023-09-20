import time
from function_record import *
from abstract_profiler import AbstractProfiler


class Profiler(AbstractProfiler):

    def __init__(self):
        super().__init__()
        self.records = {}
        self.call_stack = []

        
    
    # search a record by name
    def get_record(self, functionName):
        if functionName not in self.records:
            self.records[functionName] = FunctionRecord(functionName)
        return self.records[functionName]

    # metodo se llama cada vez que se ejecuta una funcion    
    def fun_call_start(self, functionName, args):
        super().fun_call_start(functionName, args)
        record = self.get_record(functionName)
        record.call_start_time = time.time()
        caller = None
        if self.call_stack:
            caller = self.call_stack[-1]
        record.add_caller(caller)

    def fun_call_end(self, functionName, returnValue):
        record = self.get_record(functionName)
        call_end_time = time.time()
        execution_time = call_end_time - record.call_start_time

        super().fun_call_end(functionName, returnValue)
        record.update_execution_time(execution_time)
        record.increment_frequency()
        self.call_stack.append(functionName)
    

    # print report
    def print_fun_report(self):
        print("{:<30} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10}".format('fun', 'freq', 'avg', 'max', 'min',
                                                                        'cache', 'callers'))
        for record in self.records.values():
            record.print_report()


