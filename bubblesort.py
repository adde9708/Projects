def bubble_sort(speed):
    n = len(speed)

    for i in range(n):
        for j in range(n - i - 1):
            if speed[j] > speed[j + 1]:
                speed[j], speed[j + 1] = speed[j + 1], speed[j]


speed = [100, 80, 130, 111, 96, 110, 90, 94, 86, 150, 120, 144, 146]

bubble_sort(speed)

for item in speed:
    print(item)
