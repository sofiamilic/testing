class FunctionRecord:
    def __init__(self, funName):
        self.functionName = funName
        self.frequency = 0
        self.execution_times = []
        self.callers = set()
        self.max_execution_time = 0
        self.cacheable = True

    def increment_frequency(self):
        self.frequency += 1
    
    def update_execution_time(self, elapsed_time):
        self.execution_times.append(elapsed_time)
        self.max_execution_time = max(self.max_execution_time, elapsed_time)
        


    def add_caller(self, caller):
        self.callers.add(caller)

    def set_uncacheable(self):
        self.cacheable = False

    def avg_execution_time(self):
        return sum(self.execution_times) / len(self.execution_times) if self.execution_times else 0

    def min_execution_time(self):
        return min(self.execution_times) if self.execution_times else 0
    

    def print_report(self):
        cache_status = 1 if self.cacheable else 0
        avg = "{:.3f}".format(self.avg_execution_time())
        max = "{:.3f}".format(self.max_execution_time)
        min = "{:.3f}".format(self.min_execution_time())
        print("Callers: ", self.callers)
        print("{:<30} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10}".format(self.functionName, self.frequency, avg, max, min, 0, "[]"))
