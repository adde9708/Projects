from hashlib import shake_256
from hmac import compare_digest
from math import ceil, sqrt
from secrets import SystemRandom, choice
from typing import Tuple, Union, List


def ohm_enc(message: str) -> Tuple[int, int, bytes, int]:
    key: Union[int, None] = None
    random_key: Union[int, None] = None
    real_p: Union[float, None] = None
    i: int = 0
    E: int = 0
    equations: set[Union[float, int]] = set()
    padding: bytes = b""
    res: int = 0
    message_hash: bytes = b""
    sys_random: SystemRandom = SystemRandom()

    while E == 0:
        E = sys_random.randint(-600000000000, -39081)

    i = sys_random.randint(-2000000000000, 2**448 - 1 + 2**224 - 1)
    p = i * E
    real_p = p / E
    equations = {real_p / i**2, E**2 / real_p, E / i, sqrt(i) * E}

    while key is None or key == 0:
        # Choose a random equation
        key = choice(tuple(equations))
        # Extract digits from the key
        key = int(key)
        key = hex(ceil(key))
        key = ''.join(filter(str.isdigit, key))
        key = float(key)
        key = ceil(key)

    # Generate a random initialization vector
    iv = sys_random.randbytes(64)

    # Generate a random key for xoring the hash string
    random_key = sys_random.randint(int(2 ** 256), int(2 ** 512))

    # Hash the message using SHAKE256
    message_hash = shake_256(message.encode("utf-8")).digest(512)

    # Append a fixed-length padding to the hash
    padding = b"\x80" + b"\x00" * 1024 + iv
    message_hash += padding

    # XOR the hash with the random key and the encryption key
    res = int.from_bytes(message_hash, byteorder="big") ^ random_key ^ key

    return key, random_key, iv, res


def ohm_dec(key, random_key, iv, encrypted_message, message):
    # Calculate the number of bytes needed to represent the integer
    num_bytes = (encrypted_message.bit_length() + 7) // 8

    # Decrypt the XOR result using the same keys
    decrypted_data = encrypted_message ^ random_key ^ key

    # Convert the decrypted data to bytes
    decrypted_bytes = decrypted_data.to_bytes(num_bytes, byteorder='big')

    # Extract the original message hash and IV
    original_hash_length = len(shake_256(message.encode("utf-8")).digest(512))
    message_hash = decrypted_bytes[:original_hash_length]

    # Compute the SHAKE256 hash of the original message
    original_hash = shake_256(message.encode("utf-8")).digest(
        original_hash_length)

    # Compare the message hash with the original hash
    if compare_digest(message_hash, original_hash):
        return message
    else:
        return None


def main():

    # Encrypt a message using ohm_enc
    message = "This is a secret message."
    key, random_key, iv, res = ohm_enc(message)

    # Decrypt the message using ohm_dec
    decrypted_message = ohm_dec(key, random_key, iv, res, message)

    if decrypted_message is not None:
        print("Decryption successful:")
        print("Original Message:", message)
        print("Decrypted Message:", decrypted_message)
    else:
        print("Decryption failed. The message may have been tampered with.")


main()
