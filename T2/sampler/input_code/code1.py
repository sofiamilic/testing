import time


def foo():
    bar(2, 3)
    zoo()
    time.sleep(2)
    return 2


def zoo():
    time.sleep(3)
    bar(4, 5)


def bar(a, b):
    time.sleep(1)


def main():
    foo()


main()