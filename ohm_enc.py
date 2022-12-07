import secrets
import math
import hashlib


def ohm_enc():
    E = (-39081)
    i = secrets.randbelow(2**448 - 2**224 - 1)
    p = i * E
    real_p = p / E
    key = real_p / i**2
    key2 = E**2 / real_p
    key3 = E / i
    key4 = i - E

    list_of_equations = (key, key2, key3, key4)

    key = secrets.choice(list_of_equations[0:1])
    key = str(key).replace('(', "").replace(')', "").replace(' ', "").replace(
        'e', "").replace('-', "").replace('.', "").replace(',', "")
    key = float(key)
    key = math.ceil(key)
    key = hex(key).rstrip("0")
    key = hashlib.shake_256(bytes(key, encoding='utf-8'))

    print(key.hexdigest(256))
    print()

    key2 = secrets.choice(list_of_equations[3:4])
    key2 = str(key2).replace('(', "").replace(')', "").replace(' ', "").replace(
        'e', "").replace('-', "").replace('.', "").replace(',', "")
    key2 = float(key2)
    key2 = math.ceil(key2)
    key2 = hex(key2).rstrip("0")
    key2 = hashlib.shake_256(bytes(key2, encoding='utf-8'))

    print(key2.hexdigest(256))
    print()

    key3 = secrets.choice(list_of_equations[1:2])
    key3 = str(key3).replace('(', "").replace(')', "").replace(' ', "").replace(
        'e', "").replace('-', "").replace('.', "").replace(',', "")
    key3 = float(key3)
    key3 = math.ceil(key3)
    key3 = hex(key3).rstrip("0")
    key3 = hashlib.shake_256(bytes(key3, encoding='utf-8'))

    print(key3.hexdigest(256))
    print()

    key4 = secrets.choice(list_of_equations[2:3])
    key4 = str(key4).replace('(', "").replace(')', "").replace(' ', "").replace(
        'e', "").replace('-', "").replace('.', "").replace(',', "")
    key4 = float(key4)
    key4 = math.ceil(key4)
    key4 = hex(key4).rstrip("0")
    key4 = hashlib.shake_256(bytes(key4, encoding='utf-8'))
    print(key4.hexdigest(256))
    print()


ohm_enc()

