from __future__ import print_function
import threading
from time import sleep
import traceback
from sys import _current_frames


class Sampler:
    def __init__(self, tid) -> None:
        self.tid = tid
        self.t = threading.Thread(target=self.sample, args=())
        self.active = True
        self.callContextTree = {}
        self.total_time = 0
        
    def start(self):
        self.active = True
        self.t.start()

    
    def stop(self):
        self.active = False
        
    def checkTrace(self):
        for thread_id, frames in _current_frames().items():
            if thread_id == self.tid:
                frames = traceback.walk_stack(frames)
                stack = []
                for frame, _ in frames: 
                    code = frame.f_code.co_name
                    stack.append(code)
                stack.reverse()
                print(stack)  # Esta linea imprime el stack despues de invertirlo la pueden comentar o descomentar si quieren
                self.updateCallContextTree(stack)
    
    def sample(self):
        while self.active:
            self.checkTrace()
            sleep(1)
    
    def updateCallContextTree(self, stack):
        # Este metodo debe actualizar el call context tree con la informacion del stack
        current_node = self.callContextTree
        for element in stack:
            if element not in current_node:
                current_node[element] = {"time": 0, "children": {}}
            current_node[element]["time"] += 1
            current_node = current_node[element]["children"]
        self.total_time += 1
        # print()
        # print(self.callContextTree)
        # print()

    def printReport(self, node=None, depth=1):
        # Este metodo debe imprimir el reporte del call context tree
        if node is None:
            node = self.callContextTree
        if depth == 1:
            print(f"total ({self.total_time} seconds)")
        for key, data in node.items():
            print(f"{depth*'  '} {key} ({data['time']} seconds)")
            self.printReport(data["children"], depth + 1)
