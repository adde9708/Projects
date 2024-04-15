def sum_of_even_numbers_fibonacci(num: int):
    if num < 2:
        print(0)
        return

    # initialize variables
    prev = 2
    curr = 8
    total = 2  # start with the sum of the first even Fibonacci number

    # loop through even Fibonacci numbers up to num
    while curr <= num:
        total += curr
        prev, curr = curr, 4 * curr + prev

    print(total)


sum_of_even_numbers_fibonacci(4000900)
