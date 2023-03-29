def sum_of_even_numbers_fibonacci(num: int):
    fibonacci = {1, 2}
    while max(fibonacci) + min(fibonacci) <= num:
        fibonacci.add(max(fibonacci) + min(fibonacci))
    even_numbers = {x for x in fibonacci if x % 2 == 0}
    print(sum(even_numbers))