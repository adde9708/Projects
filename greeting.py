def greeting() -> str:
    we_want_to_mess_with_greeting = False

    if we_want_to_mess_with_greeting == False:
        greeting = "Hey and thank you! I didn't get removed!"
        print(greeting)
        return greeting
    else:
        greeting = "Oh no! I got changed!"
        print(greeting)
        return greeting


greeting()
