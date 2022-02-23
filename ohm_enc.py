import secrets
import math
import hashlib


def ohm_enc():
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
    for key in list_of_equations:
        key = str(key).replace('(', "").replace(')', "").replace(' ', "").replace(
            'e', "").replace('-', "").replace('.', "").replace(',', "")
        key = float(key)

        key = math.ceil(key)

        key = hex(key)
        key = hashlib.shake_256(bytes(key, encoding='utf-8'))
        print(key.hexdigest(256))


ohm_enc()
