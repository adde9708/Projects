import time


def speed_test():
    count = 2**30  # 2^30
    start = time.time()

    # Efficient summation to trigger iteration without looping
    total = sum(range(count))

    end = time.time()
    print(f"Time taken: {end - start:.2f} seconds")
    print("Total sum:", total)


speed_test()
