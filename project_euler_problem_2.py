def sum_of_even_numbers_fibonacci(num:int):
    fibonacci = [1, 2]
    while fibonacci[-1] + fibonacci[-2] <= num:
        fibonacci.append(fibonacci[-1] + fibonacci[-2])
    fibonacci = [x for x in fibonacci if x % 2 == 0]
    print(sum(fibonacci))

sum_of_even_numbers_fibonacci(4000900)
