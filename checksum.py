import time
from typing import Tuple


def checksum(arr: Tuple) -> int:
    length: int = len(arr)
    if length == 0:
        return 0

    sum_values: Tuple[int, int, int, int] = (0, 0, 0, 0)

    sum_values = tuple(
        sum_values[j] + arr[z + i + j]
        for z in range(0, length - 256 + 1, 256)
        for i in range(0, min(256, length - z), 4)
        for j in range(4)
    )

    sum_values += tuple(
        arr[i]
        for z in range(0, length - 256 + 1, 256)
        for i in range(z + 256, min(length, z + 256))
    )

    return sum(sum_values[:4]) ^ sum(sum_values[4:])


def main():
    # Benchmarking parameters
    minSize = 1000  # Minimum size of data
    maxSize = 10000  # Maximum size of data
    step = 1000  # Step size for increasing data size

    print("Data Size\tTime (ns)")

    for dataSize in range(minSize, maxSize + 1, step):
        # Generate random data of given size
        data = tuple(range(dataSize - 1000))

        # Start the timer
        start = time.perf_counter_ns()

        # Call the function to benchmark
        big_endian_checksum = checksum(data)
        print(big_endian_checksum)
        # End the timer
        end = time.perf_counter_ns()

        # Calculate elapsed time in nanoseconds
        elapsedTime = end - start

        print(f"{dataSize}\t\t{elapsedTime}")


if __name__ == "__main__":
    main()
