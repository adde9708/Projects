def custom_square_root(x: float) -> float:
    xhalf = 0.5 * x
    xhalf = int(xhalf)
    i = x = xhalf & int(x)
    i = 0x5F3759DF - (i >> 1)
    x = float(i)
    x *= 1.5 - xhalf * x * x
    print(x)
    return x


custom_square_root(3000000)
