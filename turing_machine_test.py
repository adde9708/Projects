def turing_machine():
    i = 0
    lst = [0, 1, {10, 20, 3, 1, 4}, [0, 1]]
    while lst[i] == 0:
        lst[i] = 1

        while lst[i] == 1:
            lst[i] = 0

    return lst[2]


print(turing_machine())
