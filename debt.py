import matplotlib.pyplot as plt


def debt():

    names_of_data = ("Date ", "total", "treasury", "bonds", "swaps", "green lottery", "national", "savings", "bills", "other", "foreign", "debt", " debt in swaps")

    numbers_of_data = ["2020M11", 1136528, 678311, 176738, 31250, 20000, 2889, 5, 0, 145241, 18773, 271309, 31250]

    title = "Central government debt, balance, SEK million by item and month. "

    plt.figure(figsize=(13,13))

    plt.bar(names_of_data[1:13], numbers_of_data[1:13])

    plt.title(title + names_of_data[0] + numbers_of_data[0].rstrip())

    plt.show()


debt()
