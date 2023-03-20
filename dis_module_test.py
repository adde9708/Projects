import dis
from time import sleep

done = False


def if_statement():
    done = False

    while not done:
        done = True
        if done:
            print()
            print("done")
            print()
            sleep(2)
        else:
            return print("dead code")


if_statement()
dis.dis(if_statement)
