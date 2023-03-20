import time

a = ["Michael, William, Harper"]
b = ["John, Evelyn, Ryan"]


def trying_zip():
    print(list(zip(a, b)))


trying_zip()

print(time.process_time())
