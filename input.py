import sys
import os
from time import sleep
import pyinputplus as pypi


def loop():
    done = False
    while not done:
        c = pypi.inputStr(prompt="cmd:")
        if c == "dir":
            os.system("dir")
            sleep(1)
            sys.exit(1)

        else:
            print("command not found")
            sleep(1)
            os.system("cls")
            sys.exit()
        done = True


loop()
