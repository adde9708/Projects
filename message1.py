lst = [1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
print(lst)


def foo(msg):
    print("foo begin")
    print(msg)
    print("foo end")
    print("end import message1.py")
    msg = lambda lst: sum((lst))
    print(msg(lst))


foo("test")
