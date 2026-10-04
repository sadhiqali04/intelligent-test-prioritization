from app.cart import (
    add_to_cart,
    remove_from_cart,
    cart_total
)


def test_add_to_cart():
    cart = {}

    add_to_cart(
        cart,
        "P100",
        2
    )

    assert cart["P100"] == 2


def test_remove_from_cart():
    cart = {
        "P100": 2
    }

    remove_from_cart(
        cart,
        "P100"
    )

    assert "P100" not in cart


def test_cart_total():
    cart = {
        "P100": 2
    }

    prices = {
        "P100": 100
    }

    assert cart_total(
        cart,
        prices
    ) == 200