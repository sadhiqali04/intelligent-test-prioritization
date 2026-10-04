def check_stock(stock, requested_quantity):
    return stock >= requested_quantity


def reduce_stock(stock, quantity):
    if quantity > stock:
        return stock

    return stock - quantity


def restock(current_stock, quantity):
    return current_stock + quantity