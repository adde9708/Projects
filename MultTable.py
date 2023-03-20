def mult_table():
    for lst in [[a * b for a in range(1, 11)] for b in range(1, 11)]:
        print(lst)
    return lst


mult_table()
