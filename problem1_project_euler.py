def multiples_of_3_and_5():

    results = []

    for numbers in range(1, 1000):

        if numbers % 3 == 0 or numbers % 5 == 0:
            results.append(numbers)
            print(sum(results))


multiples_of_3_and_5()
