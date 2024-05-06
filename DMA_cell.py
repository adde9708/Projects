from typing import List, Tuple, Union


def dma_list(
    dst: int, ea_low: int, nbytes: int
) -> Union[None, Tuple[int, List[Tuple[int, int, int, int, int, int]]]]:

    result: List[Tuple[int, int, int, int, int, int]] = []
    tag_id: int = 0
    dma_list_elem: List[int] = [0, 31, 1, ea_low]
    size: int = dma_list_elem.__sizeof__()
    all_32: int = dma_list_elem[0]
    stall: int = dma_list_elem[2]
    list_size: int = nbytes * size
    aligned_ea_low = (ea_low >> 2) * 4
    dma_list_elem[0] = size + all_32

    if nbytes == 0:
        return None

    i: int = 0
    while nbytes > 0:
        sz: int = min(nbytes, 16384)
        nbytes -= sz
        ea_low += sz
        all_32 = 32
        dma_list_elem[3] = aligned_ea_low
        sz += size
        bits: int = sz >> 3

        result.append((dma_list_elem[0], tag_id, dst, bits, all_32, stall))
        i += 1

    return list_size, result


result = dma_list(0x2000, 0x1000, 1024)
print(result)
