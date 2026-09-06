from backend.repository.history_repository import (
    get_order_history,
    count_order_history
)

class HotelOrderHistoryNotFoundException(Exception):
    def __init__(self, hotel_id: int):
        self.message = (
            f"No order history found for hotel with id {hotel_id}"
        )
        super().__init__(self.message)

class InvalidDateRangeException(Exception):
    def __init__(self):
        self.message = (
            "start_time cannot be after end_time"
        )
        super().__init__(self.message)

def get_hotel_order_history(
    hotel_id: int,
    start_time=None,
    end_time=None,
    limit=20,
    offset=0
):
    # adjust it to 23:59:59 to include the entire day.
    if end_time is not None and hasattr(end_time, "hour") and end_time.hour == 0 and end_time.minute == 0 and end_time.second == 0:
        end_time = end_time.replace(hour=23, minute=59, second=59)

    # Validate time range
    if (
        start_time is not None
        and end_time is not None
        and start_time > end_time
    ):
        raise InvalidDateRangeException()


    orders = get_order_history(
        hotel_id=hotel_id,
        start_time=start_time,
        end_time=end_time,
        limit=limit,
        offset=offset
    )

    total_orders = count_order_history(
        hotel_id=hotel_id,
        start_time=start_time,
        end_time=end_time
    )

    if total_orders == 0:
        raise HotelOrderHistoryNotFoundException(
            hotel_id
        )

    return {
        "hotelId": hotel_id,
        "totalOrders": total_orders,
        "orders": orders
    }