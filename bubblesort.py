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


for item in range(len(speed)):
    print(speed[item])


print()


speed = [100, 80, 130, 111, 96, 110, 90, 94, 86, 150, 120, 144, 146]


def bubble_sort_2(speed: list):
    if len(speed) <= 1:
        return speed

    if len(speed) == 2:
        return speed if speed[0] < speed[1] else [speed[1], speed[0]]

    first_elem, second_elem, sub_array = speed[0], speed[1], speed[2:]
    result = []
    if first_elem < second_elem:
        result = [first_elem] + bubble_sort_2([first_elem] + sub_array)
    else:
        result = [second_elem] + bubble_sort_2([first_elem] + sub_array)

    return bubble_sort_2(result[:-1]) + result[-1:]


bubble_sort_2(speed)

for item in range(len(speed)):
    print(speed[item])
