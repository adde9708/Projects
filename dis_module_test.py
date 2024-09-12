import dis
from time import sleep

done = False


def if_statement():
    done = False

    while not done:
        done = True
        if not done:
            return print("dead code")
        print()
        print("done")
        print()
        sleep(2)


if_statement()
dis.dis(if_statement)
