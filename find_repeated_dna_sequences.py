from time import perf_counter_ns
from functools import reduce


def compute_initial_hash(s, nucleotide_map):
    return reduce(lambda acc, c: acc * 4 + nucleotide_map[c], s[:10], 0)


def rolling_hash(prev_hash, left_char, right_char, nucleotide_map, base):
    return ((prev_hash - nucleotide_map[left_char] * base) * 4) + nucleotide_map[
        right_char
    ]


def generate_hashes(s, nucleotide_map):
    base = 4**9
    first_hash = compute_initial_hash(s, nucleotide_map)
    return reduce(
        lambda acc, i: acc
        + [rolling_hash(acc[-1], s[i - 1], s[i + 9], nucleotide_map, base)],
        range(1, len(s) - 9),
        [first_hash],
    )


# Collect repeated substrings
def update_sets(acc, x):
    seen, repeated = acc
    return (
        (seen | {x[0]}, repeated | {x[1]})
        if x[0] in seen
        else (seen | {x[0]}, repeated)
    )


def find_repeated_dna_sequences(s):
    if len(s) < 10:
        return []

    nucleotide_map = {"A": 0, "C": 1, "G": 2, "T": 3}
    hashes = generate_hashes(s, nucleotide_map)

    # Pair each hash with its substring
    hash_to_substring = list(zip(hashes, (s[i : i + 10] for i in range(len(hashes)))))

    _, repeated = reduce(update_sets, hash_to_substring, (set(), set()))

    return list(repeated)


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
