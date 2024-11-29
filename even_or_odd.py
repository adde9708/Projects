def is_odd(num: int):
    if num % 2 == 0:
        print(f"{num}, is even")

    else:
        print(f"{num}, is odd")


def main():
    is_odd(6)
    is_odd(3)
    is_odd(116)
    is_odd(21)
    is_odd(19)


if __name__ == "__main__":
    main()
