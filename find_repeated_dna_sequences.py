from time import perf_counter_ns


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
    lst_len = len(s)

    if lst_len < 10:
        return list(ans)

    nucleotide_mapping = {"A": 1, "C": 2, "G": 3, "T": 4}
    nucleotide_mapping = [nucleotide_mapping.get(char, 0) for char in s]
    build_hash_local = build_hash
    add_hash_local = add_hash
    hash_val = build_hash_local(s, nucleotide_mapping, 0)
    hash_set = {hash_val}
    for i in range(1, lst_len - 9):
        repeated_sequence = s[i : i + 10]
        hash_val = build_hash_local(s, nucleotide_mapping, i - 1)
        add_hash_local(ans, hash_set, hash_val, repeated_sequence)

    return list(ans)


def main():
    s = "AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT"
    print("Benchmarking find_repeated_dna_sequences...")
    start_time = perf_counter_ns()
    for _ in range(1000):
        ans = find_repeated_dna_sequences(s)
        print(ans)

    print()
    end_time = perf_counter_ns()
    total_time = end_time - start_time
    print("Total time taken for 1000 iterations:", total_time, "nanoseconds")
    print("Average time taken per iteration:", total_time / 1000, "nanoseconds")


if __name__ == "__main__":
    main()
