import time


def foo():
    bar(2, 3)
    bar(4, 5)
    time.sleep(3)
    return 2


def bar(a, b):
    time.sleep(5)


def main():
    foo()


main()