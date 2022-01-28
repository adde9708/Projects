import time
import pytest

a = ["Michael, William, Harper"]
b = ["John, Evelyn, Ryan"]

c = a + b


def trying_zip():
    print(list(zip(a, b)))


trying_zip()


def test_zip():
    assert a + b == c


test_zip()
print(time.process_time())
