def potatos():

    bowl = []
    potato = "potato"
    full = False

    while not full:
        bowl.append(potato)
        if len(bowl) == 500:
            print(tuple(bowl))
            full = True
    return full


potatos()

