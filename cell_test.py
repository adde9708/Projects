from operator import mul
from typing import Tuple


def vmult(arr: Tuple[float, float, float, float, float, float, float, float],
          arr2: Tuple[float, float, float, float, float, float, float, float],
          size: int) -> Tuple[float, float, float, float, float, float,
                              float, float]:

    array_size_by_four = size // 4
    varr = arr[0:8] * array_size_by_four
    varr2 = arr2[0:8] * array_size_by_four
    vout = tuple(map(mul, varr, varr2))
    print(vout)
    return vout
