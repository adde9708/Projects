def switch():
    lst = [10 * x for x in range(10)]
    print(lst)

    s = '\t'.join(str(10 * a) for a in lst)
    print(s)


switch()
