def email_slicer() -> None:
    # Get user email address
    email = input("What is your email address:").strip()

    # Slice username
    username = email[: email.index("@")]

    # Slice domain name
    domain = email[email.index("@") + 1 :]

    # Format message
    message = (
        f"Your username is '{username}' and your domain name is '{domain}'"
    )

    # Print message
    print(message)


email_slicer()
