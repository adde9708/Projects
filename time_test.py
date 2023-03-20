import time


def for_loop():
    for i in range(1, 101):
        print(i)
    print("for loop")


def while_loop():
    x = 0
    while x < 100:
        x += 1

        print(x)
    print("while loop")


for_loop()
print(time.process_time())


while_loop()
print(time.process_time())
