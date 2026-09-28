import itertools
import struct
from hashlib import shake_256
from hmac import compare_digest
from math import isqrt
from secrets import token_bytes

MASK = 0xFFFFFFFF

W = 8
H = 8
CELLS = W * H

ROUNDS = 10
BLOCK_BYTES = 64
TAG_BYTES = 32


def u32(x: int) -> int:
    return x & MASK


def rotl(x: int, r: int) -> int:
    return u32((x << r) | (x >> (32 - r)))


def rotr(x: int, r: int) -> int:
    return u32((x >> r) | (x << (32 - r)))


def qr(a: int, b: int, c: int, d: int) -> tuple[int, int, int, int]:
    a = u32(a + b)
    d = rotl(d ^ a, 16)
    c = u32(c + d)
    b = rotl(b ^ c, 12)
    a = u32(a + b)
    d = rotl(d ^ a, 8)
    c = u32(c + d)
    b = rotl(b ^ c, 7)
    return a, b, c, d


def qr_inv(a: int, b: int, c: int, d: int) -> tuple[int, int, int, int]:
    b = rotr(b, 7) ^ c
    c = u32(c - d)
    d = rotr(d, 8) ^ a
    a = u32(a - b)
    b = rotr(b, 12) ^ c
    c = u32(c - d)
    d = rotr(d, 16) ^ a
    a = u32(a - b)
    return a, b, c, d


def mix8(v: list[int]) -> list[int]:
    a0, a1, a2, a3 = qr(v[0], v[1], v[2], v[3])
    b0, b1, b2, b3 = qr(v[4], v[5], v[6], v[7])
    return [a0, b0, a1, b1, a2, b2, a3, b3]


def mix8_inv(v: list[int]) -> list[int]:
    a0, b0, a1, b1, a2, b2, a3, b3 = v[0], v[1], v[2], v[3], v[4], v[5], v[6], v[7]
    v0, v1, v2, v3 = qr_inv(a0, a1, a2, a3)
    v4, v5, v6, v7 = qr_inv(b0, b1, b2, b3)
    return [v0, v1, v2, v3, v4, v5, v6, v7]


def ohm_words(i: int, e: int) -> list[int]:
    i &= 0xFFFF
    e &= 0xFFFF
    p = i * e
    return [
        (p // (i * i + 1)) & MASK,
        (e * e // (p + 1)) & MASK,
        (e // (i + 1)) & MASK,
        (isqrt(i) * e) & MASK,
    ]


def pack(words: list[int]) -> bytes:
    return struct.pack(f"<{len(words)}I", *words)


def init_state(key: bytes, nonce: bytes, counter: int) -> list[int]:
    kw = list(struct.unpack("<8I", key))
    nw = list(struct.unpack("<4I", nonce))

    seed = shake_256(
        pack(kw) + pack(nw) + struct.pack("<I", u32(counter))
    ).digest(CELLS * 4)

    state = list(struct.unpack(f"<{CELLS}I", seed))

    x = ohm_words(kw[0], kw[1])
    for k in range(4):
        state[(k * 8 + 4) % CELLS] = u32(state[(k * 8 + 4) % CELLS] ^ x[k])

    return state


def columns(state: list[int]) -> list[int]:
    out = state[:]
    for x in range(W):
        col = [state[y * W + x] for y in range(H)]
        col = mix8(col)
        for y in range(H):
            out[y * W + x] = col[y]
    return out


def columns_inv(state: list[int]) -> list[int]:
    out = state[:]
    for x in range(W):
        col = [state[y * W + x] for y in range(H)]
        col = mix8_inv(col)
        for y in range(H):
            out[y * W + x] = col[y]
    return out


def rows(state: list[int]) -> list[int]:
    out = state[:]
    for y in range(H):
        out[y * W : (y + 1) * W] = mix8(state[y * W : (y + 1) * W])
    return out


def rows_inv(state: list[int]) -> list[int]:
    out = state[:]
    for y in range(H):
        out[y * W : (y + 1) * W] = mix8_inv(state[y * W : (y + 1) * W])
    return out


def shear(state: list[int], k: int) -> list[int]:
    out = [0] * CELLS
    for y, x in itertools.product(range(H), range(W)):
        out[y * W + (x + y * k) % W] = state[y * W + x]
    return out


def shear_inv(state: list[int], k: int) -> list[int]:
    out = [0] * CELLS
    for y, x in itertools.product(range(H), range(W)):
        out[y * W + x] = state[y * W + (x + y * k) % W]
    return out


def engine(state: list[int]) -> list[int]:
    for r in range(ROUNDS):
        state = columns(state)
        k = 1 if r % 2 == 0 else -1
        state = shear(state, k)
        state = rows(state)
    return state


def engine_inv(state: list[int]) -> list[int]:
    for r in reversed(range(ROUNDS)):
        k = 1 if r % 2 == 0 else -1
        state = rows_inv(state)
        state = shear_inv(state, k)
        state = columns_inv(state)
    return state


def keystream(key: bytes, nonce: bytes, counter: int) -> bytes:
    return shake_256(pack(engine(init_state(key, nonce, counter)))).digest(BLOCK_BYTES)


def xor_keystream(key: bytes, nonce: bytes, data: bytes) -> bytes:
    out = bytearray()
    for n, off in enumerate(range(0, len(data), BLOCK_BYTES)):
        ks = keystream(key, nonce, n)
        chunk = data[off : off + BLOCK_BYTES]
        out += bytes(a ^ b for a, b in zip(chunk, ks))
    return bytes(out)


def new_key() -> bytes:
    return token_bytes(32)


def new_nonce() -> bytes:
    return token_bytes(16)


# ----------------------------
# Key separation and MAC
# ----------------------------


def split_keys(master: bytes) -> tuple[bytes, bytes]:
    blocks = shake_256(b"ohm-v2 keysplit" + master).digest(64)
    return blocks[:32], blocks[32:]


def compute_mac(mac_key: bytes, nonce: bytes, ct: bytes) -> bytes:
    return shake_256(
        b"ohm-v2 mac" + mac_key + nonce + struct.pack("<I", len(ct)) + ct
    ).digest(TAG_BYTES)


class AuthenticationError(Exception):
    pass


def encrypt(msg: str | bytes) -> tuple[bytes, bytes, bytes, bytes]:
    data = msg.encode() if isinstance(msg, str) else msg
    master = new_key()
    enc_key, mac_key = split_keys(master)
    nonce = new_nonce()
    ct = xor_keystream(enc_key, nonce, data)
    tag = compute_mac(mac_key, nonce, ct)
    return master, nonce, tag, ct


def decrypt(master: bytes, nonce: bytes, tag: bytes, ct: bytes) -> bytes:
    enc_key, mac_key = split_keys(master)
    if not compare_digest(compute_mac(mac_key, nonce, ct), tag):
        raise AuthenticationError("tag mismatch, refusing to decrypt")
    return xor_keystream(enc_key, nonce, ct)


def main() -> None:
    msg = "physics lattice ARX sponge cipher"
    master, nonce, tag, ct = encrypt(msg)
    pt = decrypt(master, nonce, tag, ct)

    print("cipher:  ", ct.hex())
    print("tag:     ", tag.hex())
    print("decrypted:", pt.decode())
    print("roundtrip:", "OK" if pt.decode() == msg else "FAIL")

    bad = bytearray(tag)
    bad[0] ^= 0x01
    try:
        decrypt(master, nonce, bytes(bad), ct)
        print("tamper:   FAIL, forgery accepted")
    except AuthenticationError:
        print("tamper:    OK, rejected")


if __name__ == "__main__":
    main()
