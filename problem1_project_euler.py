from typing import TypeVar

T = TypeVar('T', int, int )

def multiples_of_3_and_5() -> list[T]:
 
    results = []
    
    for numbers in range(1, 1000):

        if numbers % 3 == 0 or numbers % 5 == 0:

            results.append(numbers)
            print(sum(results))

    return results

multiples_of_3_and_5()
