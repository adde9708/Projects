def mtrr_get(n) -> int:
    phys_mask: int = 0x201 + (n * 2)
    phys_base: int = 0x200 + (n * 2)
    mask_base: int = phys_mask + phys_base
    addr = hex(0x80000000)
    target_addr = addr + str(mask_base)
    target_addr = target_addr.lstrip("0").lstrip("x").strip()
    target_addr = float(target_addr)
    target_addr = str(target_addr)
    target_addr = target_addr.rstrip("0").rstrip(".").strip()
    mask_base = mask_target = mask_base + int(target_addr)
    if mask_base == mask_target:
        print(target_addr)
        target_addr = int(target_addr)
        return target_addr in range(mask_base, mask_target)
    else:
        target_addr = int(target_addr)
        print(target_addr)
        return target_addr not in range(mask_base, mask_target)


mtrr_get(333)
