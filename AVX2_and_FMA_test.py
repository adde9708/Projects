import ctypes
from time import sleep


def avx2_and_fma():

    for j in range(3):
        i = j * 64
        dest = i + 63 * i + 63 * i + 63 - i + 63 + 2
        src = dest * 2

        print(dest)
        sleep(2)
        buf = ctypes.memset(src, dest, 0)
        print(buf)
        sleep(2)
        break

    for j in range(15):
        i = j * 16
        dst = i + 15 * i + 15 + i + 1
        print(dst)
        sleep(2)
        break


avx2_and_fma()
