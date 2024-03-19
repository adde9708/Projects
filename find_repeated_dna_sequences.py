

def add_hash(ans, hash_set, hash, repeated_sequence):
    if hash in hash_set and repeated_sequence not in ans:
        ans.add(repeated_sequence)
    else:
        hash_set.add(hash)


def build_hash(s, ans, hash_set, hash, lst_len, inp, base_power_10):
    for i in range(1, lst_len - 9):
        repeated_sequence = s[i:i+10]
        hash = hash * 4 - inp[i - 1] * base_power_10 + inp[i + 9]
        add_hash(ans, hash_set, hash, repeated_sequence)


def find_repeated_dna_sequences(s):
    ans = set()
    hash_set = set()
    hash = 0
    lst_len = len(s)
    inp = [0] * lst_len

    if lst_len < 10:
        return list(ans)

    nucleotide_mapping = {'A': 1, 'C': 2, 'G': 3, 'T': 4}

    inp = [nucleotide_mapping.get(x, 0) for x in s]

    hash = sum(inp[i] * (4 ** (9 - i)) for i in range(10))
    hash_set.add(hash)
    base_power_10 = 4 ** 10
    build_hash(s, ans, hash_set, hash, lst_len, inp, base_power_10)

    return list(ans)


s = "AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT"

ret = find_repeated_dna_sequences(s)
print(ret)
