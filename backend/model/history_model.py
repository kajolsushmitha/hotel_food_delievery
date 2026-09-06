class HotelOrderHistory:
    def __init__(
        self,
        id=None,
        hotel_id=None,
        passenger_id=None,
        order_id=None,
        order_timestamp=None,
        total_amount=None,
        items=None
    ):
        self.id = id
        self.hotel_id = hotel_id
        self.passenger_id = passenger_id
        self.order_id = order_id
        self.order_timestamp = order_timestamp
        self.total_amount = total_amount
        self.items = items
