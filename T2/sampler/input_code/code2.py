import time


def factorial(n):
    answer = 1
    time.sleep(1)
    if n > 0:
        answer = n * factorial(n-1)
    return answer


factorial(5)