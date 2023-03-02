from secrets import SystemRandom, choice
from math import sqrt, ceil
from hashlib import shake_256
from hmac import compare_digest


def ohm_enc(message):
    sys_random = SystemRandom()
    E = sys_random.randint(-600000000000, -39081)
    i = sys_random.randint(-2000000000000, 2 ** 448 - 1 + 2 ** 224 - 1)
    p = i * E
    real_p = p / E
    equations = {real_p / i ** 2, E ** 2 / real_p, E / i, sqrt(i) * E}

    # choose random equation
    key = choice(tuple(equations))

    # Extract digits from the key
    key = hex(ceil(key))
    key = ''.join(filter(str.isdigit, key))
    key = int(key)

    # Generate a random key for xoring the hash string
    random_key = sys_random.randint(int(2*256), int(2*512))

    # Hash the message using SHAKE256
    message_hash = shake_256(message.encode("utf-8")).digest(512)

    # Append a fixed-length padding to the hash
    padding = b'\x00' * 1024
    message_hash += padding

    # XOR the hash with the random key and the encryption key
    res = int.from_bytes(message_hash, byteorder='big') ^ random_key ^ key
    print(res)
    print()
    return key, random_key


ohm_enc("test")


def ohm_dec(key, random_key, encrypted):
    # Convert the encryption key to string
    key_str = hex(key)[2:]
    # Add leading zeros if necessary
    key_str = '0' * (len(key_str) % 2) + key_str
    # Convert the key string to bytes
    key_bytes = bytes.fromhex(key_str)
    # Reverse the XOR operation
    message_hash = (encrypted ^ random_key ^
                    int.from_bytes(key_bytes, byteorder='big'))
    # Remove the padding
    message_hash = message_hash[:-1024]
    # Compute the SHAKE256 hash of the original message
    original_hash = shake_256(encrypted.encode("utf-8")).digest(512)
    # Compare the message hash with the original hash
    if compare_digest(message_hash, int.from_bytes(original_hash, byteorder='big')):
        return encrypted
    else:
        return None
