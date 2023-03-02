from math import sqrt

# O(1)


def fib(n):
    print('Fibonacci series')
    phi = (1 + sqrt(5)) / 2
    Fn = round((phi ** n) / sqrt(5))
    print(Fn)


fib(10)


# O(n)
def fib(n):
    print('Fibonacci series')
    phi = (1 + sqrt(5)) / 2
    for i in range(n):
        Fn = round((phi ** i) / sqrt(5))
        print(Fn, end=' ')
    print()


fib(10)
