def greeting() -> str:
    we_want_to_mess_with_greeting = False

    if not we_want_to_mess_with_greeting:
        greeting = "Hey and thank you! I didn't get removed!"
    else:
        greeting = "Oh no! I got changed!"

    print(greeting)
    return greeting


greeting()
