class Hotel:
    def __init__(
        self,
        id=None,
        name=None,
        location=None,
        phone=None,
        is_active=True
    ):
        self.id = id
        self.name = name
        self.location = location
        self.phone = phone
        self.is_active = is_active