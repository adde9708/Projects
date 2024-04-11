def add_hash(ans, hash_set, hash_val, repeated_sequence):
    if hash_val in hash_set and repeated_sequence not in ans:
        ans.add(repeated_sequence)
    else:
        hash_set.add(hash_val)


def build_hash(s, nucleotide_mapping, start_index):
    hash_val = 0
    for i in range(10):
        hash_val += nucleotide_mapping[start_index + i] * (4 ** (9 - i))
    return hash_val


def find_repeated_dna_sequences(s):
    ans = set()
    hash_set = set()
    lst_len = len(s)

    if lst_len < 10:
        return list(ans)

    nucleotide_mapping = {'A': 1, 'C': 2, 'G': 3, 'T': 4}
    nucleotide_mapping = [nucleotide_mapping.get(char, 0) for char in s]

    hash_val = build_hash(s, nucleotide_mapping, 0)
    hash_set.add(hash_val)

    for i in range(1, lst_len - 9):
        repeated_sequence = s[i:i + 10]
        hash_val = build_hash(s, nucleotide_mapping, i - 1)
        add_hash(ans, hash_set, hash_val, repeated_sequence)

    return list(ans)


def main():
    s = "AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT"
    ans = find_repeated_dna_sequences(s)
    print(ans)


if __name__ == "__main__":
    main()
