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
    
    def sample(self):
        while self.active:
            self.checkTrace()
            sleep(1)

    def printReport(self):
        # Este metodo debe imprimir el reporte del call context tree
        pass
