import time

a = ["Martin, Adam, Jacob"]
b = ["Maria, Alma, Per"]


def test_zip():
    print(list(zip(a, b)))


test_zip()

print(a, b)

print(time.process_time())
