import re


def find_string():
    letters = "abcdefgjklmnopqrstuvwxyz"

    pat = re.sub(r"[a-z]pat?", "abcdefgjklmnopqrstuvwxyz", letters)

    print(pat)


find_string()
