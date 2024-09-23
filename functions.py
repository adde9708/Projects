def create_lst():
    empty = []
    return [90, 180, 0, empty]


def function_b():
    lst = create_lst()
    for empty in lst:
        if empty in lst:
            print(lst)


def function_a():
    lst = create_lst()
    for empty in lst:
        if empty in lst:
            print(lst)
            function_b()
            function_b()
            print(lst)


function_b()
function_a()
