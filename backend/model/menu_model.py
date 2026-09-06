class MenuItem:
    def __init__(
        self,
        id: int,
        hotelId: int,
        name: str,
        description: str,
        price,
        category: str,
        is_available: bool
    ):
        self.id = id
        self.hotelId = hotelId
        self.name = name
        self.description = description
        self.price = price
        self.category = category
        self.is_available = is_available