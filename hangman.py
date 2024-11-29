import random


class HangmanGame:

    def __init__(self, allowed_guesses=5):
        self.game_finished = False
        self.allowed_guesses = allowed_guesses
        self.incorrect_guesses_made = 0
        self.guessed_letters = set()
        self.word_to_guess = ""
        self.current_guess = ""

    def setup(self):
        self.game_finished = False
        self.incorrect_guesses_made = 0
        self.guessed_letters = set()
        self.get_word_to_guess()

    def get_possible_words(self):
        return "Monkey", "Banana", "Cacao", "Dance", "Elephant"

    def get_word_to_guess(self, possible_words=None):
        POSSIBLE_WORDS = self.get_possible_words()
        if possible_words is None:

            self.word_to_guess = random.choice(POSSIBLE_WORDS).lower()
        else:
            self.word_to_guess = random.choice(possible_words).lower()

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

    def check_valid(self, guess):

        is_alpha = guess.isalpha()

        if len(guess) != 1 or not is_alpha:
            print("\nPlease guess a single valid letter.")
            return False

        if guess in self.guessed_letters:
            print(f"\nYou've already guessed '{guess}'. Try a different letter.")
            return False

        return True

    def make_guess(self):
        while True:
            guess = input("Guess a letter or write 'q' to quit: ").lower()

            if guess == "q":

                quit()

            is_guess_valid = self.check_valid(guess)
            if is_guess_valid is not False:
                self.current_guess = guess
                self.guessed_letters.add(guess)
                break

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
    answer = input("Guess a letter or write q to quit the game: ")
    is_guess_valid = game.check_valid(answer)

    if is_guess_valid:
        while answer != "q":
            game.setup()
            while game.game_finished is not True:
                game.display_current_state()
                game.make_guess()


if __name__ == "__main__":
    main()
