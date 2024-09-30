import random

POSSIBLE_WORDS = (
    "Monkey",
    "Bananna",
    "Cacao",
    "Dance",
    "Elephant",
)


class HangmanGame:

    def __init__(self, allowed_guesses=5):
        self.game_finished = False
        self.allowed_guesses = allowed_guesses
        self.incorrect_guesses_made = 0
        self.word_to_guess = ""
        self.current_guess = ""

    def setup(self):
        self.game_finished = False
        self.incorrect_guesses_made = 0
        self.guessed_letters = set()
        self.get_word_to_guess()

    def get_word_to_guess(self, possible_words=None):
        if possible_words is not None:
            self.word_to_guess = random.choice(possible_words).lower()
        else:
            self.word_to_guess = random.choice(POSSIBLE_WORDS).lower()

    def check_guess(self):
        return self.current_guess in self.word_to_guess

    def win_or_loss_msg(self, msg):
        win_or_loss_message = f"{msg}{self.word_to_guess}"
        print(win_or_loss_message)
        quit()

    def check_game_won(self):
        for letter in self.word_to_guess:
            if letter not in self.guessed_letters:
                return
        self.win_or_loss_msg("You won! The secret word was ")

    def check_game_over(self):
        if self.incorrect_guesses_made == self.allowed_guesses:
            self.win_or_loss_msg("Game over! The secret word was ")

    def correct_guess(self):
        correct_msg = f"{self.current_guess.upper()} is in the secret word.\n"
        print(correct_msg)
        self.check_game_won()

    def incorrect_guess(self):
        incorrect_msg = f"{self.current_guess.upper()} is not in the secret word.\n"
        print(incorrect_msg)
        self.incorrect_guesses_made += 1
        self.check_game_over()

    def make_guess(self):
        guess_message = "Do you want to play again? Write quit if you want to quit: "
        guess = ""
        while guess in self.guessed_letters or not guess:
            guess = input(guess_message).lower()
            if guess == "quit":
                self.game_finished = True
                quit()

        self.guessed_letters.add(guess)
        self.current_guess = guess
        check_guess = self.check_guess()

        if check_guess:
            self.correct_guess()
        else:
            self.incorrect_guess()

        self.display_current_state()

    def display_current_state(self):
        word_info = f"The secret word is {len(self.word_to_guess)} characters long."
        print(word_info)

        if len(self.guessed_letters) > 0:
            letters_guessed = "You have guessed these letters:"
            print(letters_guessed, *sorted(tuple(self.guessed_letters)))

            wrong_guess = f"You have guessed wrong {self.incorrect_guesses_made} times."
            print(wrong_guess)

        guesses_left = (
            f"You have {self.allowed_guesses - self.incorrect_guesses_made}"
            " guesses left."
        )
        print(guesses_left)

        self.make_guess()


def main():
    game = HangmanGame()
    answer = input("Guess a letter or write quit to quit the game: ")
    while answer != "quit":
        game.setup()
        while game.game_finished is not True:
            game.display_current_state()
            game.make_guess()


if __name__ == "__main__":
    main()
