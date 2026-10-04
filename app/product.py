def get_product_price(price, quantity=1):
    return round(price * quantity, 2)


def apply_discount(price, discount_percent):
    discount = price * discount_percent / 100
    return round(price - discount, 2)


def is_product_available(stock):
    return stock > 0