from time import perf_counter_ns


def map_nucleotides():
    """Map nucleotide characters to numbers."""
    return {"A": 0, "C": 1, "G": 2, "T": 3}


def compute_base(length=10):
    """Precompute the base for rolling hash (4^(length-1))."""
    return 4 ** (length - 1)


def find_repeated_sequences(s, nucleotide_map, base, length=10):
    """Return all 10-letter-long sequences that occur more than once."""
    n = len(s)
    if n < length:
        return []

    repeated = set()
    # Compute initial hash
    h = 0
    for i in range(length):
        h = h * 4 + nucleotide_map[s[i]]
    seen = {h}

    # Rolling hash
    for i in range(1, n - length + 1):
        h = (h - nucleotide_map[s[i - 1]] * base) * 4 + nucleotide_map[
            s[i + length - 1]
        ]
        if h in seen:
            repeated.add(s[i : i + length])
        else:
            seen.add(h)

    return list(repeated)


def main():
    s = "AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT"
    nucleotide_map = map_nucleotides()
    base = compute_base(10)

    start_time = perf_counter_ns()
    for _ in range(1000):
        ans = find_repeated_sequences(s, nucleotide_map, base, 10)
        print(ans)
    end_time = perf_counter_ns()

    total_time = end_time - start_time
    print("Total time for 1000 iterations:", total_time, "ns")
    print("Average time per iteration:", total_time / 1000, "ns")


if __name__ == "__main__":
    main()
