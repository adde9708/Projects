import time

a = ["Michael, William, Harper"]
b = ["John, Evelyn, Ryan"]


def test_zip():
    print(list(zip(a, b)))


test_zip()

print(a, b)

print(time.process_time())
