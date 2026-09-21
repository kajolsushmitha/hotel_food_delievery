from pydantic import BaseModel, field_validator
from decimal import Decimal
from typing import Optional, List
from backend.schema.pass_schema import PassengerResponse
from backend.schema.hotel_schema import HotelResponse
from backend.schema.order_schema import OrderItemCreate


class PassengerLoginRequest(BaseModel):
    phone: str

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, phone: str) -> str:
        if len(phone) != 10 or not phone.isdigit():
            raise ValueError("Phone number must contain exactly 10 digits")
        return phone


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    passenger: PassengerResponse


class HotelLoginRequest(BaseModel):
    phone: str

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, phone: str) -> str:
        if len(phone) != 10 or not phone.isdigit():
            raise ValueError("Phone number must contain exactly 10 digits")
        return phone


class HotelTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    hotel: HotelResponse


class AuthenticatedOrderCreate(BaseModel):
    hotelId: int
    totalAmount: Optional[Decimal] = None
    items: Optional[List[OrderItemCreate]] = []
