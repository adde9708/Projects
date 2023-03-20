lst: tuple[int, ...] = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)


def sequential_search(lst_: tuple[int, ...], num: int) -> bool:
    for i in lst_:
        if i == num:
            print()

            print(i)

            print()
            return True
    print()

    print(f"{num} does not exist in the given list")

    print()

    return False


sequential_search(lst, 10)
