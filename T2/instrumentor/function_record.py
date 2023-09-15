class FunctionRecord:
    def __init__(self, funName):
        self.functionName = funName

    def print_report(self):
        print("{:<30} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10}".format(self.functionName, 0, 0, 0, 0, 0, "[]"))
