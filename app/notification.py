def send_email(email, message):
    if "@" not in email:
        return False

    if not message:
        return False

    return True


def send_order_notification(email, order_id):
    return send_email(
        email,
        f"Order {order_id} has been created"
    )