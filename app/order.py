def create_order(user_id, cart):
    if not cart:
        return None

    return {
        "user_id": user_id,
        "items": cart,
        "status": "created"
    }


def update_order_status(order, status):
    valid_statuses = {
        "created",
        "paid",
        "shipped",
        "delivered",
        "cancelled"
    }

    if status not in valid_statuses:
        return False

    order["status"] = status
    return True