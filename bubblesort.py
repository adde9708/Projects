def bubble_sort(speed):
    n = len(speed)
    swapped = True

    while swapped:
        swapped = False
        for i in range(1, n):
            if speed[i - 1] > speed[i]:
                speed[i - 1], speed[i] = speed[i], speed[i - 1]
                swapped = True


speed = [100, 80, 130, 111, 96, 110, 90, 94, 86, 150, 120, 144, 146]
bubble_sort(speed)

for item in speed:
    print(item)
