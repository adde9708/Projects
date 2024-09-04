# Första versionen av vårt spel kommer vara simplistiskt men fortfarande ett
# fungerande program. Under kommande veckor kommer vi lägga till fler funktioner
# samt dela upp programmet i flera filer.
import random

POSSIBLE_WORDS = (
    "Apa",
    "Banan",
    "Cacao",
    "Dans",
    "Elefant",
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
        print("Du vann! Det hemliga ordet var", self.word_to_guess)
        quit()

    def check_game_over(self):
        if self.incorrect_guesses_made == self.allowed_guesses:
            print("Game over! Det hemliga ordet var", self.word_to_guess)
            quit()

    def correct_guess(self):
        print(self.current_guess.upper(), "finns i det hemliga ordet.\n")
        self.check_game_won()

    def incorrect_guess(self):
        print(self.current_guess.upper(), "finns inte i det hemliga ordet.\n")
        self.incorrect_guesses_made += 1
        self.check_game_over()

    def display_current_state(self):
        print("Det hemliga ordet är", len(self.word_to_guess), "tecken långt.")
        if len(self.guessed_letters) > 0:
            print("Du har gissat dessa bokstäver:", self.guessed_letters)
            print("Du har gissat fel", self.incorrect_guesses_made, "gånger.")
        print(
            "Du har",
            self.allowed_guesses - self.incorrect_guesses_made,
            "gissningar kvar.",
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
