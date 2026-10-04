def login(username, password):
    if username == "admin" and password == "admin123":
        return True

    return False


def logout(username):
    return f"{username} logged out"


def validate_token(token):
    return token.startswith("TOKEN-") and len(token) > 10