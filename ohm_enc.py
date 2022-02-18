import secrets


def ohm_enc():
    for _ in range(12):
        E = 277
        i = secrets.randbelow(935104938709281475457689481226)
        p = i * E
        real_p = p / E
        keys = []
        key = real_p / i**2
        key2 = E**2 / real_p
        key3 = E / i

        list_of_equations = (key, key2, key3)

        for _ in list_of_equations:
            keys.append(list_of_equations)
            key = secrets.choice(keys)
            print(key)


ohm_enc()
