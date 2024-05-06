from math import sqrt


# O(1)
def fib_const_time(n: int):
    print("Fibonacci series")
    phi: float = (1 + sqrt(5)) / 2
    Fn: int = round((phi**n) / sqrt(5))
    print(Fn)


fib_const_time(10)


# O(n)
def fib(n: int):
    print("Fibonacci series")
    phi: float = (1 + sqrt(5)) / 2
    for i in range(n):
        Fn: int = round((phi**i) / sqrt(5))
        print(Fn, end=" ")
    print()


fib(10)
