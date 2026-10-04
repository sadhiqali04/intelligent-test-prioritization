from app.payment import (
    calculate_total,
    process_payment,
    refund_payment
)


def test_payment_total():
    assert calculate_total(
        100
    ) == 118


def test_custom_tax():
    assert calculate_total(
        200,
        0.10
    ) == 220


def test_process_payment():
    assert process_payment(
        500
    ) is True


def test_invalid_payment():
    assert process_payment(
        0
    ) is False


def test_refund():
    assert refund_payment(
        500
    ) is True