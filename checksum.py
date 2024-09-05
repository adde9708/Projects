import time
from typing import Tuple


# Function to convert an integer to big-endian format (4 bytes only)
def convert_to_big_endian(number: int) -> bytes:
    return number.to_bytes(4, byteorder="big")


def calculate_checksum(data: Tuple[int, ...]) -> int:
    data_length = len(data)
    if data_length == 0:
        return 0

    # Ensure that the length of the data is a multiple of 4 for alignment
    data_length_aligned = (
        (data_length + 3) // 4 * 4
    )  # Round up to the nearest multiple of 4
    padded_data = data + (0,) * (data_length_aligned - data_length)

    # Calculate checksum
    checksum = 0
    for i in range(0, data_length_aligned, 4):
        # Create a 4-byte integer from the slice using arithmetic operations
        word = (
            padded_data[i] * 16777216  # 256^3
            + padded_data[i + 1] * 65536  # 256^2
            + padded_data[i + 2] * 256  # 256^1
            + padded_data[i + 3]  # 256^0
        )
        checksum += word

        # Use modulo to ensure checksum fits in 4 bytes
        checksum %= 0x100000000  # 2^32
        checksum = convert_to_big_endian(checksum)
        checksum = int.from_bytes(checksum, byteorder="big")

    return checksum


# Main function to run the benchmark
def main() -> None:
    min_data_size = 1000  # Minimum size of data
    max_data_size = 10000  # Maximum size of data
    size_step = 1000  # Step size for increasing data size

    print("Data Size\tTime (ns)")

    for current_size in range(min_data_size, max_data_size + 1, size_step):
        # Generate data of given size
        generated_data = tuple(i for i in range(current_size))

        # Start the timer
        start_time = time.time_ns()

        # Call the function to benchmark
        calculated_checksum = calculate_checksum(generated_data)

        # End the timer
        end_time = time.time_ns()

        # Calculate elapsed time in nanoseconds
        elapsed_time = end_time - start_time

        # Print the results in hex format for clarity
        print(f"{current_size}\t\t{elapsed_time}\tChecksum: {calculated_checksum}")


if __name__ == "__main__":
    main()
