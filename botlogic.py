import random
def generate_password(length):
    password_symbols = "+-/*!&$#?=@abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    password = ""
    for i in range(length):
        password += random.choice(password_symbols)
    return password
def smash_bash(password):
    letters=list(password)
    random.shuffle(letters)
    return "".join(letters)