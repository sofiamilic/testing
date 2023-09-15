import time


def main():
    foo()
    bar()
    zoo()


def foo():
    for _ in range(10):
        bar()
        time.sleep(1)


def zoo():
    foo()


def bar():
    time.sleep(1)


main()
