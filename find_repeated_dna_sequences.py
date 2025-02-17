from time import perf_counter_ns


def create_hash(s, nucleotide_mapping, hash_val):
    for i in range(10):
        hash_val = (hash_val * 4) + nucleotide_mapping[s[i]]
    return {hash_val}


def compute_rolling_hash(s, lst_len, nucleotide_mapping, hash_set, ans):
    base = 4**9  # Precompute highest power of 4
    hash_val = 0
    for i in range(1, lst_len - 9):
        hash_val = (
            (hash_val - nucleotide_mapping[s[i - 1]] * base) * 4
        ) + nucleotide_mapping[s[i + 9]]

        if hash_val in hash_set:
            repeated_sequence = s[i : i + 10]
            ans.add(repeated_sequence)
        else:
            hash_set.add(hash_val)


def find_repeated_dna_sequences(s):
    ans = set()
    lst_len = len(s)
    if lst_len < 10:
        return []

    nucleotide_mapping = {"A": 0, "C": 1, "G": 2, "T": 3}
    hash_val = 0

    # Initial hash computation for first 10 characters
    hash_set = create_hash(s, nucleotide_mapping, hash_val)

    # Compute rolling hash for the rest of the string
    compute_rolling_hash(s, lst_len, nucleotide_mapping, hash_set, ans)

    return list(ans)


def main():

    s = "AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT"
    print("Benchmarking find_repeated_dna_sequences...")
    start_time = perf_counter_ns()

    for _ in range(1000):
        ans = find_repeated_dna_sequences(s)
        print(ans)

    end_time = perf_counter_ns()
    total_time = end_time - start_time
    print("Total time taken for 1000 iterations:", total_time, "nanoseconds")
    print("Average time taken per iteration:", total_time / 1000, "nanoseconds")


if __name__ == "__main__":
    main()
