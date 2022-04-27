import secrets
import math
import hashlib
import gc


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
    keys.append(list_of_equations)
    x = tuple(keys)
    for list_of_equations in x:
        key = secrets.choice(keys)

        key2 = secrets.choice(keys)
        key2 = str(key2).replace('(', "").replace(')', "").replace(' ', "").replace(
            'e', "").replace('-', "").replace('.', "").replace(',', "")
        key2 = float(key2)
        key2 = math.ceil(key2)
        key2 = hex(key2).rstrip("0")
        key2 = hashlib.shake_256(bytes(key2, encoding='utf-8'))
        print(key2.hexdigest(256))
        key3 = secrets.choice(keys)
        key3 = str(key3).replace('(', "").replace(')', "").replace(' ', "").replace(
            'e', "").replace('-', "").replace('.', "").replace(',', "")
        key3 = float(key3)
        key3 = math.ceil(key3)
        key3 = hex(key3).rstrip("0")
        key3 = hashlib.shake_256(bytes(key3, encoding='utf-8'))
        print(key3.hexdigest(256))
        key = str(key).replace('(', "").replace(')', "").replace(' ', "").replace(
            'e', "").replace('-', "").replace('.', "").replace(',', "")
        key = float(key)
        key = math.ceil(key)
        key = hex(key).rstrip("0")
        key = hashlib.shake_256(bytes(key, encoding='utf-8'))
        print(key.hexdigest(256))


ohm_enc()

