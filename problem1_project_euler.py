def multiples_of_3_and_5(n: int) -> int:
    numbers = set(range(3, n, 3)) | set(range(5, n, 5))

    total_sum = sum(numbers)
    return print(total_sum)


multiples_of_3_and_5(1000)
