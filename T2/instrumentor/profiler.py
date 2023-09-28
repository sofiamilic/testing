import time
from function_record import *
from abstract_profiler import AbstractProfiler


class Profiler(AbstractProfiler):

    def __init__(self):
        super().__init__()
        self.records = {}
        self.callers = {}
        self.return_values = {}
        self.arg_values = {}


        
    
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
        record.current_args = args
    
        
        

    def fun_call_end(self, functionName, returnValue):
        record = self.get_record(functionName)
        call_end_time = time.time()
        execution_time = call_end_time - record.call_start_time
        super().fun_call_end(functionName, returnValue)
        record.update_execution_time(execution_time)
        record.increment_frequency()
        record.callers = self.callers[functionName]
        #print("Funcion: ", functionName, "Cacheable: ", record.cacheable,"Args", record.current_args, "Return value: ", returnValue)

        if record.cacheable:
            if functionName not in self.arg_values:
                self.arg_values[functionName] = record.current_args
                self.return_values[functionName] = returnValue
            else:
                if self.arg_values[functionName] != record.current_args:
                    record.set_uncacheable()
                else:
                    if self.return_values[functionName] != returnValue:
                        record.set_uncacheable()
        
                

        

    def get_callers(self, code):
        #print("Aca ingrese a mi nueva funcion")
        dict = {}
        actual_function = ""
        in_function = False
        for line in code.splitlines():
            if "def" in line:
                actual_function = line.split(" ")[1].split("(")[0]
                dict[actual_function] = []
        
        for line in code.splitlines():
            if "def" in line:
                actual_function = line.split(" ")[1].split("(")[0]
                in_function = True
            elif "Profiler.record_end" in line:
                in_function = False
            elif "Profiler.record_start" in line:
                pass
            else:
                if in_function:
                    for key in dict.keys():
                        if key in line and key != actual_function and actual_function not in dict[key]:
                            dict[key].append(actual_function)
                        if key in line and key == actual_function and actual_function not in dict[key]:
                            dict[key].append(actual_function)

                    
        self.callers = dict
        

    

    # print report
    def print_fun_report(self):
        print("{:<30} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10}".format('fun', 'freq', 'avg', 'max', 'min',
                                                                        'cache', 'callers'))
        for record in self.records.values():
            record.print_report()


