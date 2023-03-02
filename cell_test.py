from operator import mul
from typing import Tuple


def vmult(arr: Tuple[float, float, float, float, float, float, float, float],
          arr2: Tuple[float, float, float, float, float, float, float, float],
          size: int) -> Tuple[float, float, float, float, float, float,
                              float, float]:

    array_size_by_four = size >> 2
    varr = arr[:7] * array_size_by_four
    varr2 = arr2[:8] * array_size_by_four
    vout = tuple(map(mul, varr, varr2))
    print(vout)
    return vout


vmult((2.2, 4.2, 8.2, 16.2, 32.2, 64.2, 128.2, 256.2),
      (2.4, 4.4, 8.4, 16.4, 32.4, 64.4, 128.4, 256.4), 8)
