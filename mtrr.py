def mtrr_get(n: int) -> bool:
    phys_mask: int = 0x201 + (n * 2)  # physical mask address
    phys_base: int = 0x200 + (n * 2)   # physical base address
    mask_base: int = phys_base & phys_mask  # mask for base address
    addr = 0x80000000
    target_addr: int = addr & mask_base

    if mask_base == target_addr:
        print(target_addr)
        return target_addr in range(mask_base, mask_base + (2 ** 12))
    else:
        print(target_addr)
        return target_addr not in range(mask_base, mask_base + (2 ** 12))


mtrr_get(333)
