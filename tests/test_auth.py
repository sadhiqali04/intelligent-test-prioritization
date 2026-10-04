from app.auth import (
    login,
    logout,
    validate_token
)


def test_valid_login():
    assert login(
        "admin",
        "admin123"
    ) is True


def test_invalid_login():
    assert login(
        "admin",
        "wrong"
    ) is False


def test_logout():
    assert logout(
        "admin"
    ) == "admin logged out"


def test_valid_token():
    assert validate_token(
        "TOKEN-123456"
    ) is True