from secrets import choice


def play():
    win = False
    lose = False
    score = 0
    highscore_lst = []

    name = input("What's your name? ")

    player_choice = input("Rock, paper or scissors? ").lower()
    choices = ("rock", "paper", "scissors")

    if player_choice in choices:

        computer_choice = choice(choices)

        if player_choice == computer_choice:
            print("\nDraw, try again")

        elif (player_choice == choices[0]
              and computer_choice == choices[2]
              or player_choice == choices[1]
              and computer_choice == choices[0]
              or player_choice == choices[2]
              and computer_choice == choices[1]):

            win = True
        else:
            lose = True

        if win:
            print("\nYou won")
            score += 1
        elif lose:
            print("\nYou lost, try again")

        highscore_lst.append((name, score))
    else:
        print("\nInvalid choice. Please try again")

    return highscore_lst


def view_users():
    highscore_lst = play()
    print("\nHighscore list\n")
    for name, score in highscore_lst:
        print(f"{name}: {score}")


def main():
    while True:
        print("\nMenu:")
        print("1. Do you want to play?")
        print("2. Highscore")
        print("3. Exit")

        player_choice = input("Enter your choice: ")
        choices = ("1", "2", "3")

        if player_choice == choices[0]:
            play()
        elif player_choice == choices[1]:
            view_users()
        elif player_choice == choices[2]:
            break
        else:
            print("\nInvalid choice. Please try again.")


if __name__ == "__main__":
    main()
