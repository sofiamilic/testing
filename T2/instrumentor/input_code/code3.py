import time


def foo():
    for _ in range(10):
        bar()
        time.sleep(3)


def bar():
    time.sleep(1)


foo()