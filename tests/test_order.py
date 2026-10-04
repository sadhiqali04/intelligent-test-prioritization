from app.order import (
    create_order,
    update_order_status
)


def test_create_order():
    cart = {
        "P100": 2
    }

    order = create_order(
        "USER1",
        cart
    )

    assert order["status"] == "created"


def test_empty_order():
    order = create_order(
        "USER1",
        {}
    )

    assert order is None


def test_update_order():
    order = {
        "user_id": "USER1",
        "status": "created"
    }

    assert update_order_status(
        order,
        "paid"
    ) is True

    assert order["status"] == "paid"