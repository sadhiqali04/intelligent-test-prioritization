from app.notification import (
    send_email,
    send_order_notification
)


def test_send_email():
    assert send_email(
        "user@example.com",
        "Hello"
    ) is True


def test_invalid_email():
    assert send_email(
        "invalid",
        "Hello"
    ) is False


def test_order_notification():
    assert send_order_notification(
        "user@example.com",
        "ORD1001"
    ) is True