import time

def for_loop():
    print("for loop")
    for i in range(1, 101):
        print(i)

def while_loop():
    print("while loop")
    x = 0
    while x < 100:
        x+=1
        print(x)

for_loop()
print(time.process_time())
while_loop()
print(time.process_time())
