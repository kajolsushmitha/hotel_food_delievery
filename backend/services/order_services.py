from decimal import Decimal
from backend.repository import order_repository, pass_repository, menu_repository


ALLOWED_STATUSES = {
    "PENDING",
    "CONFIRMED",
    "PREPARING",
    "READY",
    "DELIVERED",
    "CANCELLED"
}


def create_order(order_data):
    # 1. Resolve passenger by name or id
    passenger = None
    if getattr(order_data, "passengerName", None):
        passenger = pass_repository.get_passenger_by_name(order_data.passengerName)
        if not passenger:
            raise ValueError(f"Passenger with name '{order_data.passengerName}' not found")
        passenger_id = passenger.id
    elif getattr(order_data, "passengerId", None):
        passenger = pass_repository.get_passenger_by_id(order_data.passengerId)
        if not passenger:
            raise ValueError(f"Passenger with id {order_data.passengerId} not found")
        passenger_id = passenger.id
    else:
        raise ValueError("Passenger name is required to place an order")

    # 2. Check if hotel exists
    if not menu_repository.hotel_exists(order_data.hotelId):
        raise ValueError(f"Hotel with id {order_data.hotelId} not found")

    # 3. Calculate total amount and validate order items
    total_amount = Decimal("0.00")
    if hasattr(order_data, "items") and order_data.items:
        for item in order_data.items:
            if item.quantity <= 0:
                raise ValueError("Item quantity must be greater than 0")

            menu_item = menu_repository.get_menu_item_by_id(item.menuItemId)
            if not menu_item:
                raise ValueError(f"Menu item with id {item.menuItemId} not found")

            if menu_item["hotelId"] != order_data.hotelId:
                raise ValueError(
                    f"Menu item '{menu_item['name']}' (ID: {item.menuItemId}) does not belong to hotel {order_data.hotelId}"
                )

            # Auto calculate price and subtotal using database menu item price
            item.price = Decimal(str(menu_item["price"]))
            item.subtotal = item.price * item.quantity
            total_amount += item.subtotal
    elif getattr(order_data, "totalAmount", None) is not None:
        total_amount = Decimal(str(order_data.totalAmount))

    return order_repository.create_order(
        order_data=order_data,
        passenger_id=passenger_id,
        hotel_id=order_data.hotelId,
        total_amount=total_amount,
        items=order_data.items or []
    )


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

