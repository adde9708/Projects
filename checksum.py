import time


def checksum(arr: bytearray) -> int:
    length: int = len(arr)
    if length == 0:
        return 0

    sum_values: bytearray = bytearray([0] * 4)

    sum_values = bytearray(
        [
            sum_values[j] + arr[z + i + j]
            for z in range(0, length - 256 + 1, 256)
            for i in range(0, min(256, length - z), 4)
            for j in range(4)
        ]
    )

    sum_values += bytearray(
        [
            arr[i]
            for z in range(0, length - 256 + 1, 256)
            for i in range(z + 256, min(length, z + 256))
        ]
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
        data = bytearray(dataSize - 1000)

        # Start the timer
        start = time.perf_counter()

        # Call the function to benchmark
        checksum = checksum(data)
        print(checksum)
        # End the timer
        end = time.perf_counter()

        # Calculate elapsed time in nanoseconds
        elapsedTime = end - start

        print(f"{dataSize}\t\t{elapsedTime}")


if __name__ == "__main__":
    main()
