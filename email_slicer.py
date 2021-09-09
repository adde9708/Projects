# Get user email address
email = input("What is your email address:").strip()

# Slice username
username = email[:email.index("@")]

# Slice domain name
domain = email[email.index("@") + 1:]

# Format message
message = "Your username is '{}' and your domain name is '{}'".format(username, domain)

# Print message
print(message)
