from backend.repository import order_repository


ALLOWED_STATUSES = {
    "PENDING",
    "CONFIRMED",
    "PREPARING",
    "READY",
    "DELIVERED",
    "CANCELLED"
}


def create_order(order_data):
    return order_repository.create_order(order_data)


def get_all_orders():
    return order_repository.get_all_orders()


def get_order_by_id(order_id: int):
    order = order_repository.get_order_by_id(order_id)

    if not order:
        raise ValueError("Order not found")

    return order


def get_orders_by_passenger(passenger_id: int):
    return order_repository.get_orders_by_passenger(
        passenger_id
    )


def get_orders_by_hotel(hotel_id: int):
    return order_repository.get_orders_by_hotel(
        hotel_id
    )


def update_order_status(order_id: int, status: str):

    status = status.upper()

    if status not in ALLOWED_STATUSES:
        raise ValueError(
            f"Invalid status. Allowed values: "
            f"{', '.join(ALLOWED_STATUSES)}"
        )

    order = order_repository.update_order_status(
        order_id,
        status
    )

    if not order:
        raise ValueError("Order not found")

    return order


def delete_order(order_id: int):

    deleted = order_repository.delete_order(order_id)

    if not deleted:
        raise ValueError("Order not found")

    return True


def cleanup_expired_orders(days: int = 30):
    if days < 1:
        raise ValueError("Days must be a positive integer (e.g., at least 1 day)")

    deleted_orders = order_repository.delete_expired_orders(days)
    deleted_ids = [order["id"] for order in deleted_orders]
    deleted_count = len(deleted_orders)

    if deleted_count == 0:
        message = f"No orders found older than {days} days to delete"
    else:
        message = f"Successfully cleaned up {deleted_count} expired order(s) older than {days} days"

    return {
        "message": message,
        "deletedCount": deleted_count,
        "deletedOrderIds": deleted_ids,
        "deletedOrders": deleted_orders,
        "daysThreshold": days
    }

