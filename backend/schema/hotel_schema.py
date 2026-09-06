from pydantic import BaseModel


class HotelCreate(BaseModel):
    name: str
    location: str
    phone: str
    is_active: bool = True


class HotelUpdate(BaseModel):
    name: str | None = None
    location: str | None = None
    phone: str | None = None
    is_active: bool | None = None


class HotelResponse(BaseModel):
    id: int
    name: str
    location: str
    phone: str
    is_active: bool