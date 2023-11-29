from operator import mul


def vmult(
    arr: tuple[float, float, float, float, float, float, float, float],
    arr2: tuple[float, float, float, float, float, float, float, float],
    size: int,
) -> tuple[float, float, float, float, float, float, float, float]:
    array_size_by_four = size >> 2
    varr = arr[:7] * array_size_by_four
    varr2 = arr2[:8] * array_size_by_four
    vout = tuple(map(mul, varr, varr2))
    print(vout)
    return vout


def main():
    vout = vmult(
        (2.2, 4.2, 8.2, 16.2, 32.8, 64.2, 128.2, 256.2),
        (2.8, 4.8, 8.8, 16.8, 32.8, 64.8, 128.8, 256.8),
        8,
    )

    for i in range(len(vout)):
        print(vout[i])


main()
