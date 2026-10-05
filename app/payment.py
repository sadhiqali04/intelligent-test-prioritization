def calculate_total(amount, tax_rate=0.18):
    return round(
        amount + (amount * tax_rate),
        2
    )


def process_payment(amount):
    if amount <= 0:
        return False

    return amount >= 1


def refund_payment(amount):
    if amount <= 0:
        return False

    return True