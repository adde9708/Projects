from secrets import choice


class Words:
    POSSIBLE_WORDS: tuple = ("Monkey", "Banana", "Cacao", "Dance", "Elefant")


class HangManGame:
    def __init__(self, allowed_guesses: int = 5) -> None:
        self.allowed_guesses = allowed_guesses
        self.incorrect_guesses_made = 0
        self.word_to_guess = ""
        self.guessed_letters = set()
        self.current_guess = ""
        self.revealed_word = ""
        self.setup()

    def setup(self):
        self.incorrect_guesses_made = 0
        self.guessed_letters = set()
        self.word_to_guess = choice(Words.POSSIBLE_WORDS).lower()
        self.revealed_word = "_" * len(self.word_to_guess)
        print("Welcome to Hangman!")
        self.display_current_state()

    def display_all_guesses(self):
        print("You have guessed these letters:", *sorted(list(self.guessed_letters)))

    def guesses_left(self):
        print(
            "You have",
            self.allowed_guesses - self.incorrect_guesses_made,
            "guesses left.",
        )

    def display_current_state(self):
        print("\nWord: ", self.display_secret())
        if len(self.guessed_letters) > 0:
            self.display_all_guesses()
            print("You have guessed wrong", self.incorrect_guesses_made, "times.")
        self.guesses_left()

        if not self.check_game_over() and not self.check_game_won():
            self.make_guess()

    def make_guess(self):
        guess = input("Guess a letter: ").lower()
        if not guess.isalpha() or len(guess) != 1:
            print("Please enter a single valid letter.")
            return self.display_current_state()

        if guess in self.guessed_letters:
            print("You already guessed that letter.")
            return self.display_current_state()

        self.guessed_letters.add(guess)
        self.current_guess = guess

        if self.check_guess():
            self.correct_guess()
        else:
            self.incorrect_guess()

        self.display_current_state()

    def check_guess(self):
        return self.current_guess in self.word_to_guess

    def correct_guess(self):
        print(f"Good guess! '{self.current_guess}' is in the word.")
        new_revealed = list(self.revealed_word)
        for i in range(len(self.word_to_guess)):
            if self.word_to_guess[i] == self.current_guess:
                new_revealed[i] = self.current_guess
        self.revealed_word = "".join(new_revealed)

    def incorrect_guess(self):
        print(f"Sorry, '{self.current_guess}' is not in the word.")
        self.incorrect_guesses_made += 1

    def check_game_won(self):
        if "_" not in self.revealed_word:
            print(f"\n Congratulations! You guessed the word: {self.word_to_guess}")
            return True
        return False

    def check_game_over(self):
        if self.incorrect_guesses_made >= self.allowed_guesses:
            print(f"\n Game over! The word was: {self.word_to_guess}")
            return True
        return False

    def display_secret(self):
        return " ".join(self.revealed_word)


def main():
    HangManGame()


if __name__ == "__main__":
    main()
