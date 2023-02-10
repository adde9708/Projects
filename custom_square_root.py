def custom_square_root(x) -> float:
    xhalf = 0.5 * x
    xhalf = int(xhalf)
    i = x = xhalf & int(x)
    i = 0x5f3759df - (i >> 1)
    x = float(i)
    x = x * (1.5 - xhalf * x * x)
    return print(x)


custom_square_root(3000000)
