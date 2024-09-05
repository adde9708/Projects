from hashlib import shake_256
from hmac import compare_digest
from math import ceil, sqrt
from secrets import SystemRandom
from typing import Optional, Tuple, Union


def check_if_message_is_string(message) -> str:
    if isinstance(message, str):
        return message
    else:
        raise TypeError("message must be a string")


def ohm_enc(message: str) -> Tuple[float, int, bytes, int]:
    key: Union[float, str] = 0.0
    random_key: Union[float, int] = 0
    real_p: Union[float, int] = 0.0
    i: int = 0
    E: int = 0
    equations: set[Union[float, str]] = set()
    padding: bytes = b""
    res: int = 0
    message_hash: bytes = b""
    sys_random: SystemRandom = SystemRandom()

    E = sys_random.randint(-600000000000, -39081)
    i = sys_random.randint(2, 2**448 - 1 + 2**224 - 1)
    p = i * E
    real_p = p / E
    equations = {real_p / i**2, E**2 / real_p, E / i, sqrt(i) * E}
    message = check_if_message_is_string(message)

    equations = {real_p / i**2, E**2 / real_p, E / i, sqrt(i) * E}
    while key is None or key == 0:

        # Choose a random equation
        key = sys_random.choice(tuple(equations))

        # Extract digits from the key
        key = float(key)
        key = hex(ceil(key))
        key = "".join(filter(str.isdigit, key))
        key = int(key)

    # Generate a random initialization vector
    iv = sys_random.randbytes(64)

    # Generate a random key for xoring the hash string
    random_key = sys_random.randint(int(2**256), int(2**512))

    # Hash the message using SHAKE256
    message_hash = shake_256(message.encode("utf-8")).digest(512)

    # Append a fixed-length padding to the hash
    padding = b"\x80" + b"\x00" * 1024 + iv
    message_hash += padding

    # Convert the key to int
    key = int(key)

    # XOR the hash with the random key and the encryption key
    res = int.from_bytes(message_hash, byteorder="big") ^ random_key ^ key

    return key, random_key, iv, res


def ohm_dec(
    key: float, random_key: int, iv: bytes, encrypted_message: int, message: str
) -> Optional[str]:

    # Calculate the number of bytes needed to represent the integer
    num_bytes = (encrypted_message.bit_length() + 7) // 8

    # Decrypt the XOR result using the same keys
    decrypted_data = encrypted_message ^ random_key ^ int(key)

    # Convert the decrypted data to bytes
    decrypted_bytes = decrypted_data.to_bytes(num_bytes, byteorder="big")

    # Compute the SHAKE256 hash of the original message
    original_hash = shake_256(message.encode("utf-8")).digest(512)
    original_hash_length = len(original_hash)

    # Extract the original message hash and IV
    message_hash = decrypted_bytes[:original_hash_length]

    return message if compare_digest(message_hash, original_hash) else None


def main() -> None:

    # Encrypt the message using ohm_enc
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


if __name__ == "__main__":
    main()
