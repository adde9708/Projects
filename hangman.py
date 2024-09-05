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
        self.allowed_guesses = allowed_guesses
        self.word_to_guess = ""
        self.current_guess = ""

    def setup(self):
        # Here should some parts of __init__ be to shorten the function.
        # This can also be used to reset the game
        self.incorrect_guesses_made = 0
        self.guessed_letters = set()
        self.get_word_to_guess()
        self.display_current_state()

    def get_word_to_guess(self):
        self.word_to_guess = random.choice(POSSIBLE_WORDS).lower()

    def check_guess(self):
        return self.current_guess in self.word_to_guess

    def check_game_won(self):
        for letter in self.word_to_guess:
            if letter not in self.guessed_letters:
                return
        print("You won! The secret word was", self.word_to_guess)
        quit()

    def check_game_over(self):
        if self.incorrect_guesses_made == self.allowed_guesses:
            print("Game over! The secret word was", self.word_to_guess)
            quit()

    def correct_guess(self):
        print(self.current_guess.upper(), "is in the secret word.\n")
        self.check_game_won()

    def incorrect_guess(self):
        print(self.current_guess.upper(), "is not in the secret word.\n")
        self.incorrect_guesses_made += 1
        self.check_game_over()

    def display_current_state(self):
        print("Det hemliga ordet är", len(self.word_to_guess), "tecken långt.")
        if len(self.guessed_letters) > 0:
            print("You have guessed these letters:", self.guessed_letters)
            print("You have guessd wrong ", self.incorrect_guesses_made, "gånger.")
        print(
            "You have",
            self.allowed_guesses - self.incorrect_guesses_made,
            "guesses left.",
        )
        self.make_guess()

    def make_guess(self):
        guess = input("Gissa en bokstav: ").lower()
        self.guessed_letters.add(guess)
        self.current_guess = guess
        check_correct = self.check_guess()

        if check_correct is True:
            self.correct_guess()
        else:
            self.incorrect_guess()

        self.display_current_state()


if __name__ == "__main__":
    game = HangmanGame()
