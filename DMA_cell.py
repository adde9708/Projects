from typing import Any, Union, Tuple, List


def dma_list(dst: hex, ea_low: int, nbytes: int) -> Union[Tuple[None], Tuple[int, List[Tuple[int, int, Any, int, int, int]]]]:
    all_32: int = 0
    unsigned_bytes: int = 31
    unsigned_stall: int = 1
    tag_id: int = 0
    dma_list_elem: List[int] = [all_32, unsigned_bytes, unsigned_stall, ea_low]
    size: int = dma_list_elem.__sizeof__()
    all_32 = dma_list_elem[0]
    stall = dma_list_elem[2]

    if nbytes == 0:
        return None

    i: int = 0
    list_size: int = nbytes * size
    result: List[Tuple[int, int, Any, int, int, int]] = []
    while nbytes > 0:
        sz: int = min(nbytes, 16384)
        dma_list_elem[3] = ea_low
        dma_list_elem[0] = size + all_32
        nbytes -= sz
        ea_low += sz
        all_32 = 32

        sz += size
        bits: int = sz // 8

        result.append((dma_list_elem[0], tag_id, dst, bits, all_32, stall))
        i += 1

    return list_size, result


result = dma_list(0x2000, 0x1000, 1024)
print(result)
