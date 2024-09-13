from hashlib import shake_256
from hmac import compare_digest
from math import ceil, sqrt
from secrets import SystemRandom
from typing import Optional, Set, Tuple, Union


# Function to check if the message is a string
def check_if_message_is_string(message: Union[str, bytes]) -> str:
    if isinstance(message, str):
        return message
    else:
        raise TypeError("message must be a string")


# Function to initialize the SystemRandom object
def initialize_sys_random() -> SystemRandom:
    return SystemRandom()


# Function to initialize the variables
def initialize_variables() -> Tuple[int, int, Union[float, int], Union[float, str], Union[float, int]]:
    key: Union[float, str] = 0.0
    random_key: Union[float, int] = 0
    real_p: Union[float, int] = 0.0
    i: int = 0
    E: int = 0
    return i, E, real_p, key, random_key


# Function to initialize equations
def initialize_equations() -> Tuple[Set[Union[float, str]], bytes, bytes, int]:
    equations: Set[Union[float, str]] = set()
    padding: bytes = b""
    message_hash: bytes = b""
    res: int = 0
    return equations, padding, message_hash, res


# Function to generate the equations set
def generate_equations(
    i: int, E: int, real_p: Union[float, int]
) -> Set[Union[float, str]]:
    return {real_p / i**2, E**2 / real_p, E / i, sqrt(i) * E}


# Encryption function
def ohm_enc(message: str) -> Tuple[float, int, bytes, int]:

    # Check so it's a string so it doesn't crash if someone decides
    # to try and use ints as message. Because encode doesn't work
    # with any other types except string
    message = check_if_message_is_string(message)

    # Initialize SystemRandom
    sys_random = initialize_sys_random()

    # Initialize the variables
    i, E, real_p, key, random_key = initialize_variables()
    equations, padding, message_hash, res = initialize_equations()

    # Generate random values for i and E
    E = sys_random.randint(-600000000000, -39081)
    i = sys_random.randint(2, 2**448 - 1 + 2**224 - 1)
    p = i * E
    real_p = p / E

    # Generate equations based on i, E, and real_p
    equations = generate_equations(i, E, real_p)

    # Choose a random key from the equations
    while key is None or key == 0:
        key = sys_random.choice(tuple(equations))
        key = float(key)
        key = hex(ceil(key))
        key = "".join(filter(str.isdigit, key))
        key = int(key)

    # Generate a random initialization vector (IV)
    iv: bytes = sys_random.randbytes(64)

    # Generate a random key for XORing the hash string
    random_key = sys_random.randint(int(2**256), int(2**512))

    # Hash the message using SHAKE256
    message_hash = shake_256(message.encode("utf-8")).digest(512)

    # Append a fixed-length padding to the hash
    padding = b"\x80" + b"\x00" * 1024 + iv
    message_hash += padding

    # XOR the hash with the random key and the encryption key
    res = int.from_bytes(message_hash, byteorder="big") ^ random_key ^ int(key)

    return float(key), random_key, iv, res


# Decryption function
def ohm_dec(
    key: float, random_key: int, iv: bytes, encrypted_message: int, message: str
) -> Optional[str]:
    # Calculate the number of bytes needed to represent the integer
    num_bytes: int = (encrypted_message.bit_length() + 7) // 8

    # Decrypt the XOR result using the same keys
    decrypted_data: int = encrypted_message ^ random_key ^ int(key)

    # Convert the decrypted data to bytes
    decrypted_bytes: bytes = decrypted_data.to_bytes(num_bytes, byteorder="big")

    # Compute the SHAKE256 hash of the original message
    original_hash: bytes = shake_256(message.encode("utf-8")).digest(512)
    original_hash_length: int = len(original_hash)

    # Extract the original message hash and IV
    message_hash: bytes = decrypted_bytes[:original_hash_length]

    return message if compare_digest(message_hash, original_hash) else None


# Main function
def main() -> None:
    # Encrypt the message using ohm_enc
    message: str = "This is a secret message."
    key, random_key, iv, res = ohm_enc(message)

    # Decrypt the message using ohm_dec
    decrypted_message: Optional[str] = ohm_dec(key, random_key, iv, res, message)

    if decrypted_message is not None:
        print("Decryption successful:")
        print("Original Message:", message)
        print("Decrypted Message:", decrypted_message)
    else:
        print("Decryption failed. The message may have been tampered with.")


if __name__ == "__main__":
    main()
