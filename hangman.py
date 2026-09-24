import random


# -------------------------
# State initialization
# -------------------------
def init_game_state(allowed_guesses=5, possible_words=None):
    if possible_words is None:
        possible_words = ("Monkey", "Banana", "Cacao", "Dance", "Elephant")

    word = random.choice(possible_words).lower()
    return {
        "game_finished": False,
        "allowed_guesses": allowed_guesses,
        "incorrect_guesses_made": 0,
        "guessed_letters": frozenset(),
        "word_to_guess": word,
    }


# -------------------------
# Pure functions (no side effects)
# -------------------------
def is_guess_valid(guess, guessed_letters):
    guess_is_alpha = guess.isalpha()
    if len(guess) != 1 or not guess_is_alpha:
        return False, "Please guess a single valid letter."
    if guess in guessed_letters:
        return False, f"You've already guessed '{guess}'. Try a different letter."
    return True, None


def check_guess(word, guess):
    return guess in word


def check_game_won(state):
    word = state["word_to_guess"]
    guessed_letters = state["guessed_letters"]

    # Check if each letter in the word has been guessed
    all_guessed = all(letter in guessed_letters for letter in word)

    if all_guessed:
        new_state = {**state, "game_finished": True}
        print(f"You won! The secret word was {word}")
        return new_state

    return state


def check_game_over(state):
    if state["incorrect_guesses_made"] >= state["allowed_guesses"]:
        new_state = {**state, "game_finished": True}
        print(f"Game over! The secret word was {state['word_to_guess']}")
        return new_state
    return state


def apply_guess(state, guess):
    guessed_letters = state["guessed_letters"] | frozenset({guess})
    if check_guess(state["word_to_guess"], guess):
        print(f"{guess.upper()} is in the secret word.\n")
        state = {**state, "guessed_letters": guessed_letters}
        return check_game_won(state)
    else:
        print(f"{guess.upper()} is not in the secret word.\n")
        state = {
            **state,
            "guessed_letters": guessed_letters,
            "incorrect_guesses_made": state["incorrect_guesses_made"] + 1,
        }
        return check_game_over(state)


# -------------------------
# I/O functions
# -------------------------
def display_state(state):
    print(f"The secret word is {len(state['word_to_guess'])} characters long.")
    if state["guessed_letters"]:
        print("You have guessed these letters:", *sorted(state["guessed_letters"]))
        print(f"You have guessed wrong {state['incorrect_guesses_made']} times.")
    guesses_left = state["allowed_guesses"] - state["incorrect_guesses_made"]
    print(f"You have {guesses_left} guesses left.\n")


def prompt_guess(state):
    while True:
        guess = input("Guess a letter or write 'q' to quit: ").lower()
        if guess == "q":
            exit()
        valid, msg = is_guess_valid(guess, state["guessed_letters"])
        if valid:
            return guess
        else:
            print(msg)


# -------------------------
# Game loop
# -------------------------
def play_game():
    state = init_game_state()
    while not state["game_finished"]:
        display_state(state)
        guess = prompt_guess(state)
        state = apply_guess(state, guess)


if __name__ == "__main__":
    play_game()
