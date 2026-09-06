class Order:
    def __init__(
        self,
        id=None,
        passengerId=None,
        hotelId=None,
        totalAmount=None,
        status=None,
        orderTime=None
    ):
        self.id = id
        self.passengerId = passengerId
        self.hotelId = hotelId
        self.totalAmount = totalAmount
        self.status = status
        self.orderTime = orderTime