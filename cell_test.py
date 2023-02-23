from operator import mul
from typing import TypeVar


T = TypeVar('T', float, float)


def vmult(arr: tuple[T, T, T, T, T, T, T, T],
          arr2: tuple[T, T, T, T, T, T, T, T], size: int) -> int:

    array_size_by_four = size >> 2
    varr = arr[0:7] * array_size_by_four
    varr2 = arr2[0:8] * array_size_by_four

    for _ in range(array_size_by_four):
        vout = tuple(map(mul, varr, varr2))
        print(vout)
        return 0

    return 0


vmult((2.2, 4.4, 8.2, 16.4, 32.4, 64.4, 128.4, 256.4),
      (2.4, 4.8, 8.8, 16.8, 32.8, 64.8, 128.8, 256.8), 8)
