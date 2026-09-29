from dataclasses import dataclass
from hashlib import shake_256
from hmac import compare_digest
from math import isqrt
from secrets import token_bytes
from struct import pack, unpack


@dataclass(frozen=True)
class Constants:
    MASK = 0xFFFFFFFF
    W = 8
    H = 8
    CELLS = W * H
    ROUNDS = 10
    BLOCK_BYTES = 64
    TAG_BYTES = 32


def u32(x: int) -> int:
    return x & Constants.MASK


def qr(a: int, b: int, c: int, d: int) -> tuple[int, int, int, int]:
    m = Constants.MASK
    a = (a + b) & m
    t = d ^ a
    d = ((t << 16) | (t >> 16)) & m
    c = (c + d) & m
    t = b ^ c
    b = ((t << 12) | (t >> 20)) & m
    a = (a + b) & m
    t = d ^ a
    d = ((t << 8) | (t >> 24)) & m
    c = (c + d) & m
    t = b ^ c
    b = ((t << 7) | (t >> 25)) & m
    return a, b, c, d


def qr_inv(a: int, b: int, c: int, d: int) -> tuple[int, int, int, int]:
    m = Constants.MASK
    b = (((b >> 7) | (b << 25)) & m) ^ c
    c = (c - d) & m
    d = (((d >> 8) | (d << 24)) & m) ^ a
    a = (a - b) & m
    b = (((b >> 12) | (b << 20)) & m) ^ c
    c = (c - d) & m
    d = (((d >> 16) | (d << 16)) & m) ^ a
    a = (a - b) & m
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
    m = Constants.MASK
    return [
        (p // (i * i + 1)) & m,
        (e * e // (p + 1)) & m,
        (e // (i + 1)) & m,
        (isqrt(i) * e) & m,
    ]


def pack_words(words: list[int]) -> bytes:
    return pack(f"<{len(words)}I", *words)


def init_state(key: bytes, nonce: bytes, counter: int) -> list[int]:
    c = Constants.CELLS
    kw = list(unpack("<8I", key))
    nw = list(unpack("<4I", nonce))
    seed = shake_256(
        pack_words(kw) + pack_words(nw) + pack("<I", u32(counter))
    ).digest(c * 4)

    state = list(unpack(f"<{c}I", seed))

    x = ohm_words(kw[0], kw[1])
    for k in range(4):
        pos = (k * 8 + 4) % c
        state[pos] = u32(state[pos] ^ x[k])

    return state


def columns(state: list[int]) -> list[int]:
    w = Constants.W
    h = Constants.H
    out = state[:]

    for x in range(w):
        col = [state[y * w + x] for y in range(h)]
        col = mix8(col)
        for y in range(h):
            out[y * w + x] = col[y]
    return out


def columns_inv(state: list[int]) -> list[int]:
    w = Constants.W
    h = Constants.H
    out = state[:]

    for x in range(w):
        col = [state[y * w + x] for y in range(h)]
        col = mix8_inv(col)
        for y in range(h):
            out[y * w + x] = col[y]
    return out


def rows(state: list[int]) -> list[int]:
    w = Constants.W
    h = Constants.H
    out = state[:]

    for y in range(h):
        lo = y * w
        out[lo : lo + w] = mix8(state[lo : lo + w])
    return out


def rows_inv(state: list[int]) -> list[int]:
    w = Constants.W
    h = Constants.H
    out = state[:]

    for y in range(h):
        lo = y * w
        out[lo : lo + w] = mix8_inv(state[lo : lo + w])
    return out


def shear(state: list[int], k: int) -> list[int]:
    w = Constants.W
    h = Constants.H
    out = [0] * Constants.CELLS

    for y in range(h):
        lo = y * w
        row = state[lo : lo + w]
        s = (y * k) % w
        if s:
            row = row[w - s :] + row[: w - s]
        out[lo : lo + w] = row
    return out


def shear_inv(state: list[int], k: int) -> list[int]:
    w = Constants.W
    h = Constants.H
    out = [0] * Constants.CELLS

    for y in range(h):
        lo = y * w
        row = state[lo : lo + w]
        s = (y * k) % w
        if s:
            row = row[s:] + row[:s]
        out[lo : lo + w] = row
    return out


def round_step(state: list[int], k: int) -> list[int]:
    m = Constants.MASK
    c = Constants.CELLS
    buf = state[:]
    out = [0] * c
    for x in range(8):
        c0 = state[x]
        c1 = state[8 + x]
        c2 = state[16 + x]
        c3 = state[24 + x]
        c4 = state[32 + x]
        c5 = state[40 + x]
        c6 = state[48 + x]
        c7 = state[56 + x]

        a0 = (c0 + c1) & m
        t = c3 ^ a0
        a3 = ((t << 16) | (t >> 16)) & m
        a2 = (c2 + a3) & m
        t = c1 ^ a2
        a1 = ((t << 12) | (t >> 20)) & m
        a0 = (a0 + a1) & m
        t = a3 ^ a0
        a3 = ((t << 8) | (t >> 24)) & m
        a2 = (a2 + a3) & m
        t = a1 ^ a2
        a1 = ((t << 7) | (t >> 25)) & m

        b0 = (c4 + c5) & m
        t = c7 ^ b0
        b3 = ((t << 16) | (t >> 16)) & m
        b2 = (c6 + b3) & m
        t = c5 ^ b2
        b1 = ((t << 12) | (t >> 20)) & m
        b0 = (b0 + b1) & m
        t = b3 ^ b0
        b3 = ((t << 8) | (t >> 24)) & m
        b2 = (b2 + b3) & m
        t = b1 ^ b2
        b1 = ((t << 7) | (t >> 25)) & m

        buf[x] = a0
        buf[8 + x] = b0
        buf[16 + x] = a1
        buf[24 + x] = b1
        buf[32 + x] = a2
        buf[40 + x] = b2
        buf[48 + x] = a3
        buf[56 + x] = b3

    for y in range(8):
        o = y * 8
        s = (-y * k) % 8
        c0 = buf[o + (0 + s) % 8]
        c1 = buf[o + (1 + s) % 8]
        c2 = buf[o + (2 + s) % 8]
        c3 = buf[o + (3 + s) % 8]
        c4 = buf[o + (4 + s) % 8]
        c5 = buf[o + (5 + s) % 8]
        c6 = buf[o + (6 + s) % 8]
        c7 = buf[o + (7 + s) % 8]

        a0 = (c0 + c1) & m
        t = c3 ^ a0
        a3 = ((t << 16) | (t >> 16)) & m
        a2 = (c2 + a3) & m
        t = c1 ^ a2
        a1 = ((t << 12) | (t >> 20)) & m
        a0 = (a0 + a1) & m
        t = a3 ^ a0
        a3 = ((t << 8) | (t >> 24)) & m
        a2 = (a2 + a3) & m
        t = a1 ^ a2
        a1 = ((t << 7) | (t >> 25)) & m

        b0 = (c4 + c5) & m
        t = c7 ^ b0
        b3 = ((t << 16) | (t >> 16)) & m
        b2 = (c6 + b3) & m
        t = c5 ^ b2
        b1 = ((t << 12) | (t >> 20)) & m
        b0 = (b0 + b1) & m
        t = b3 ^ b0
        b3 = ((t << 8) | (t >> 24)) & m
        b2 = (b2 + b3) & m
        t = b1 ^ b2
        b1 = ((t << 7) | (t >> 25)) & m

        out[o + 0] = a0
        out[o + 1] = b0
        out[o + 2] = a1
        out[o + 3] = b1
        out[o + 4] = a2
        out[o + 5] = b2
        out[o + 6] = a3
        out[o + 7] = b3
    return out


def engine(state: list[int]) -> list[int]:
    rounds = Constants.ROUNDS

    for r in range(rounds):
        k = 1 if r % 2 == 0 else -1
        state = round_step(state, k)
    return state


def engine_inv(state: list[int]) -> list[int]:
    rounds = Constants.ROUNDS
    for r in reversed(range(rounds)):
        k = 1 if r % 2 == 0 else -1
        state = rows_inv(state)
        state = shear_inv(state, k)
        state = columns_inv(state)
    return state


def keystream(key: bytes, nonce: bytes, counter: int) -> bytes:
    block_bytes = Constants.BLOCK_BYTES
    state = engine(init_state(key, nonce, counter))
    return shake_256(pack_words(state)).digest(block_bytes)


def xor_keystream(key: bytes, nonce: bytes, data: bytes) -> bytes:
    block_bytes = Constants.BLOCK_BYTES
    out = bytearray()
    for n, off in enumerate(range(0, len(data), block_bytes)):
        ks = keystream(key, nonce, n)
        chunk = data[off : off + block_bytes]
        out += bytes(a ^ b for a, b in zip(chunk, ks))
    return bytes(out)


def new_key() -> bytes:
    return token_bytes(32)


def new_nonce() -> bytes:
    return token_bytes(16)


# ----------------------------
# Key separation and MAC
# ----------------------------


class AuthenticationError(Exception):
    pass


def split_keys(master: bytes) -> tuple[bytes, bytes]:
    blocks = shake_256(b"ohm-v2 keysplit" + master).digest(64)
    return blocks[:32], blocks[32:]


def compute_mac(mac_key: bytes, nonce: bytes, ct: bytes) -> bytes:

    tag_bytes = Constants.TAG_BYTES
    return shake_256(
        b"ohm-v2 mac" + mac_key + nonce + pack("<I", len(ct)) + ct
    ).digest(tag_bytes)


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
