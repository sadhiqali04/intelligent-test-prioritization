from app.user import (
    create_user,
    get_user_role,
    update_email
)


def test_create_user():
    user = create_user(
        "alice",
        "alice@example.com"
    )

    assert user["username"] == "alice"


def test_admin_role():
    assert get_user_role(
        "admin"
    ) == "administrator"


def test_unknown_role():
    assert get_user_role(
        "unknown"
    ) == "unknown"


def test_update_email():
    user = {
        "username": "alice",
        "email": "old@example.com"
    }

    assert update_email(
        user,
        "new@example.com"
    ) is True