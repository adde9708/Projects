from math import sqrt


def fib(n):
    print('Fibonacci series')
    phi = (1 + sqrt(5)) / 2
    Fn = round((phi ** n) / sqrt(5))
    print(Fn)


fib(100)
