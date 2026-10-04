def create_user(username, email):
    if not username or not email:
        return False

    return {
        "username": username,
        "email": email
    }


def get_user_role(username):
    roles = {
        "admin": "administrator",
        "alice": "customer",
        "bob": "customer"
    }

    return roles.get(username, "unknown")


def update_email(user, new_email):
    if "@" not in new_email:
        return False

    user["email"] = new_email
    return True