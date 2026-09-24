import random


class HangmanGame:
    def __init__(self, allowed_guesses=5):
        self.allowed_guesses = allowed_guesses
        self.game_finished = False
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
        return ["Monkey", "Banana", "Cacao", "Dance", "Elephant"]

    def get_word_to_guess(self, possible_words=None):
        words = self.get_possible_words() if possible_words is None else possible_words
        self.word_to_guess = random.choice(words).lower()

    def check_guess(self):
        return self.current_guess in self.word_to_guess

    def win_or_loss_msg(self, msg):
        print(f"{msg}{self.word_to_guess}")
        self.game_finished = True

    def check_game_won(self):
        if all(letter in self.guessed_letters for letter in self.word_to_guess):
            self.win_or_loss_msg("You won! The secret word was ")

    def check_game_over(self):
        if self.incorrect_guesses_made >= self.allowed_guesses:
            self.win_or_loss_msg("Game over! The secret word was ")

    def correct_guess(self):
        print(f"{self.current_guess.upper()} is in the secret word.\n")
        self.check_game_won()

    def incorrect_guess(self):
        print(f"{self.current_guess.upper()} is not in the secret word.\n")
        self.incorrect_guesses_made += 1
        self.check_game_over()

    def check_valid(self, guess):
        if len(guess) != 1 or not guess.isalpha():
            print("\nPlease guess a single valid letter.")
            return False

        if guess in self.guessed_letters:
            print(f"\nYou've already guessed '{guess}'. Try a different letter.")
            return False

        return True

    def make_guess(self):
        while True:
            guess = input("Guess a letter or type 'q' to quit: ").lower()
            if guess == "q":
                print("Thanks for playing!")
                exit()

            if self.check_valid(guess):
                self.current_guess = guess
                self.guessed_letters.add(guess)
                break

        if self.check_guess():
            self.correct_guess()
        else:
            self.incorrect_guess()

    def display_current_state(self):
        print(f"\nThe secret word has {len(self.word_to_guess)} characters.")

        if self.guessed_letters:
            print("You have guessed these letters:", *sorted(self.guessed_letters))
            print(f"Wrong guesses: {self.incorrect_guesses_made}")

        guesses_left = self.allowed_guesses - self.incorrect_guesses_made
        print(f"You have {guesses_left} guesses left.\n")


def main():
    game = HangmanGame()

    while True:
        game.setup()

        while not game.game_finished:
            game.display_current_state()
            game.make_guess()

        again = input("Play again? (y/n): ").lower()
        if again != "y":
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
