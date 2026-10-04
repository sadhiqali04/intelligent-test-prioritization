from app.inventory import (
    check_stock,
    reduce_stock,
    restock
)


def test_check_stock():
    assert check_stock(
        10,
        5
    ) is True


def test_insufficient_stock():
    assert check_stock(
        2,
        5
    ) is False


def test_reduce_stock():
    assert reduce_stock(
        10,
        3
    ) == 7


def test_restock():
    assert restock(
        5,
        10
    ) == 15