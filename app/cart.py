def add_to_cart(cart, product_id, quantity):
    cart[product_id] = cart.get(product_id, 0) + quantity
    return cart


def remove_from_cart(cart, product_id):
    if product_id in cart:
        del cart[product_id]

    return cart


def cart_total(cart, prices):
    total = 0

    for product_id, quantity in cart.items():
        total += prices[product_id] * quantity

    return round(total, 2)