import time
from function_record import *
from abstract_profiler import AbstractProfiler


class Profiler(AbstractProfiler):

    def __init__(self):
        self.records = {}
    
    # search a record by name
    def get_record(self, functionName):
        if functionName not in self.records:
            self.records[functionName] = FunctionRecord(functionName)
        return self.records[functionName]

    # metodo se llama cada vez que se ejecuta una funcion    
    def fun_call_start(self, functionName, args):
        record = self.get_record(functionName)
       
    def fun_call_end(self, functionName, returnValue):
        pass
    
    # print report
    def print_fun_report(self):
        print("{:<30} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10}".format('fun', 'freq', 'avg', 'max', 'min',
                                                                        'cache', 'callers'))
        for record in self.records.values():
            record.print_report()


