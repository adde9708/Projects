import secrets
import math
import hashlib


def ohm_enc():
    # smallest constant(nothing up my sleeve number, check ed448)
    E = (-39081)

    # prime base(it's the prime that ed448 uses)
    i = secrets.randbelow(2**448 - 2**224 - 1)
    # equations from ohms law
    p = i * E
    real_p = p / E
    key = real_p / i**2
    key2 = E**2 / real_p
    key3 = E / i
    key4 = math.sqrt(i) * E
    # put all equations inside a tuple
    list_of_equations = (key, key2, key3, key4)
    # pick random key from the tuple as key1 (index 1 to index2)
    key = secrets.choice(list_of_equations[1:2])
    # convert number to string
    key = str(key).replace('(', "").replace(')', "").replace(' ', "").replace(
        'e', "").replace('-', "").replace('.', "").replace(',', "").replace("+", "")
    # convert str to float so that math.ceil works
    key = float(key)
    # always round up
    key = math.ceil(key)
    # convert to hex for some extra obfuscation and strip away trailing zeros
    key = hex(key).rstrip("0")
    # hash the hex value with SHAKE256(check ed448)
    key = hashlib.shake_256(bytes(key, encoding='utf-8'))
    # print out the hash (512 bits which is the number of bits for SHAKE256)
    print(key.hexdigest(512))
    print()

    # pick random key from the tuple (index 3 to index 5)
    key2 = secrets.choice(list_of_equations[3:5])
    # the rest is exactly the same as key 1
    key2 = str(key2).replace('(', "").replace(')', "").replace(' ', "").replace(
        'e', "").replace('-', "").replace('.', "").replace(',', "").replace('+', "")
    key2 = float(key2)
    key2 = math.ceil(key2)
    key2 = hex(key2).rstrip("0")
    key2 = hashlib.shake_256(bytes(key2, encoding='utf-8'))

    print(key2.hexdigest(512))
    print()
    # pick random key from the tuple(index 0 to index1)
    key3 = secrets.choice(list_of_equations[0:1])
    # the rest is exactly the same as key 1
    key3 = str(key3).replace('(', "").replace(')', "").replace(' ', "").replace(
        'e', "").replace('-', "").replace('.', "").replace(',', "").replace("+", "")
    key3 = float(key3)
    key3 = math.ceil(key3)
    key3 = hex(key3).rstrip("0")
    key3 = hashlib.shake_256(bytes(key3, encoding='utf-8'))

    print(key3.hexdigest(512))
    print()
    # pick random key from the tuple(index 2 to index 3)
    key4 = secrets.choice(list_of_equations[2:3])
    # the rest is exactly the same as key 1
    key4 = str(key4).replace('(', "").replace(')', "").replace(' ', "").replace(
        'e', "").replace('-', "").replace('.', "").replace(',', "").replace("+", "")
    key4 = float(key4)
    key4 = math.ceil(key4)
    key4 = hex(key4).rstrip("0")
    key4 = hashlib.shake_256(bytes(key4, encoding='utf-8'))
    print(key4.hexdigest(512))
    print()


ohm_enc()
