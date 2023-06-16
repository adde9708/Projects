from timeit import default_timer as timer

start = timer()


def calculate_packing(n: int):
    if n == 1:
        return 1
    else:
        total = 1
        i = 2
        while i <= n:
            total += calculate_packing(n >> i)
            i *= 2
        return total % 1020202009


result = calculate_packing(24_680)
print(result)
end = timer()
print(end - start)
