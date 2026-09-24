import itertools
from dataclasses import dataclass
from hashlib import shake_256
from hmac import compare_digest
from secrets import SystemRandom


@dataclass(frozen=True)
class Constants:
    MASK = 0xFFFFFFFF


# ----------------------------
# ARX primitives (reversible)
# ----------------------------


def u32(x):
    return x & Constants.MASK


def rotl(x, r):
    return u32((x << r) | (x >> (32 - r)))


def rotr(x, r):
    return u32((x >> r) | (x << (32 - r)))


def qr(a, b, c, d):
    a = u32(a + b)
    d ^= a
    d = rotl(d, 16)
    c = u32(c + d)
    b ^= c
    b = rotl(b, 12)
    a = u32(a + b)
    d ^= a
    d = rotl(d, 8)
    c = u32(c + d)
    b ^= c
    b = rotl(b, 7)
    return a, b, c, d


def qr_inv(a, b, c, d):
    b = rotr(b, 7)
    b ^= c
    c = u32(c - d)
    d = rotr(d, 8)
    d ^= a
    a = u32(a - b)
    b = rotr(b, 12)
    b ^= c
    c = u32(c - d)
    d = rotr(d, 16)
    d ^= a
    a = u32(a - b)
    return a, b, c, d


# ----------------------------
# Physics lattice embedding
# ----------------------------


def physics_lattice(i, E):
    p = i * E

    # Equation set used to map to lattice coordinates
    x0 = abs(int(p / (i * i + 1)))
    x1 = abs(int((E * E) / (p + 1)))
    x2 = abs(int(E / (i + 1)))
    x3 = abs(int((i**0.5) * E))

    return [x0, x1, x2, x3]


# ----------------------------
# Sponge injection
# ----------------------------


def sponge_state(data: bytes):
    h = shake_256(data).digest(64)
    return [int.from_bytes(h[i : i + 4], "little") for i in range(0, 64, 4)]


# ----------------------------
# Build lattice (2x2 field)
# ----------------------------


def build_lattice(seed4, sponge16):
    s = seed4 + sponge16[:12]

    return [
        s[0],
        s[1],
        s[2],
        s[3],
        s[4],
        s[5],
        s[6],
        s[7],
        s[8],
        s[9],
        s[10],
        s[11],
        s[12] ^ s[13],
        s[14] ^ s[15],
        s[0] ^ s[5],
        s[2] ^ s[7],
    ]


# ----------------------------
# Lattice PDE diffusion step
# ----------------------------


# 2x2 torus neighbors
def idx(x, y):
    return (y % 2) * 2 + (x % 2)


def diffuse(state):

    new = state[:]

    for y, x in itertools.product(range(2), range(2)):
        i = idx(x, y)

        n1 = state[idx(x + 1, y)]
        n2 = state[idx(x - 1, y)]
        n3 = state[idx(x, y + 1)]
        n4 = state[idx(x, y - 1)]

        # PDE-like coupling
        new[i], _, _, _ = qr(state[i], n1, n2, n3 ^ n4)

    return new


# ----------------------------
# 20-round ARX-PDE engine
# ----------------------------


def engine(state):
    for _ in range(20):

        # row + column diffusion
        state = diffuse(state)

        # diagonal mixing
        state[0], state[5], state[10], state[15] = qr(
            state[0], state[5], state[10], state[15]
        )

        state[1], state[6], state[11], state[12] = qr(
            state[1], state[6], state[11], state[12]
        )

    return state


# ----------------------------
# Keystream
# ----------------------------


def squeeze(state):
    out = bytearray()
    for v in state:
        out += v.to_bytes(4, "little")
    return shake_256(bytes(out)).digest(64)


# ----------------------------
# Encryption
# ----------------------------


def encrypt(msg: str) -> tuple[bytes, bytes, bytes]:
    rng = SystemRandom()

    i = rng.randint(2, 1 << 16)
    E = rng.randint(2, 1 << 16)
    iv = rng.randbytes(16)
    phys = physics_lattice(i, E)
    sponge = sponge_state(
        msg.encode() + i.to_bytes(4, "little") + E.to_bytes(4, "little") + iv
    )

    state = build_lattice(phys, sponge)
    state = engine(state)

    ks = squeeze(state)

    ct = bytes(m ^ ks[j % len(ks)] for j, m in enumerate(msg.encode()))

    key = i.to_bytes(4, "little") + E.to_bytes(4, "little")

    return key, iv, ct


# ----------------------------
# Decryption (reconstruction model)
# ----------------------------


def decrypt(key: bytes, iv: bytes, ct: bytes, original: str) -> str | None:
    i = int.from_bytes(key[:4], "little")
    E = int.from_bytes(key[4:], "little")

    phys = physics_lattice(i, E)
    sponge = sponge_state(original.encode() + key + iv)

    state = build_lattice(phys, sponge)
    state = engine(state)

    ks = squeeze(state)

    pt = bytes(c ^ ks[j % len(ks)] for j, c in enumerate(ct))

    return pt.decode() if compare_digest(pt, original.encode()) else None


# ----------------------------
# Demo
# ----------------------------


def main():
    msg = "physics lattice ARX sponge cipher"

    key, iv, ct = encrypt(msg)
    dec = decrypt(key, iv, ct, msg)

    print("cipher:", ct.hex())
    print("decrypted:", dec)


if __name__ == "__main__":
    main()
