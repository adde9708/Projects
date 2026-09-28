def foo():
    global a
    a = "hello"


foo()

b = "cat"


def bar():
    b = "dog"
    print(a)
    print(b)


bar()
