lst = [90, 180, 0]
empty = []
lst.append(empty)


def function_a():
    for empty in lst:
        if empty in lst:
            print(lst)
            function_b()
            function_b()
            print(lst)


def function_b():
    for empty in lst:
        if empty in lst:
            print(lst)


function_b()
function_a()
