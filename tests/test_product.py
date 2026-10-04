from app.product import (
    get_product_price,
    apply_discount,
    is_product_available
)


def test_product_price():
    assert get_product_price(
        100,
        2
    ) == 200


def test_discount():
    assert apply_discount(
        100,
        10
    ) == 90


def test_product_available():
    assert is_product_available(
        10
    ) is True


def test_product_unavailable():
    assert is_product_available(
        0
    ) is False