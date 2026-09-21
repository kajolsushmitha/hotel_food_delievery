from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime
from typing import Optional, List


class OrderItemCreate(BaseModel):
    menuItemId: int
    quantity: int
    price: Optional[Decimal] = None
    subtotal: Optional[Decimal] = None


class OrderCreate(BaseModel):
    passengerName: str
    hotelId: int
    #passengerId: Optional[int] = None
    #totalAmount: Optional[Decimal] = None
    items: List[OrderItemCreate] = []


class OrderStatusUpdate(BaseModel):
    status: str


class OrderResponse(BaseModel):
    id: int
    passengerId: int
    passengerName: Optional[str] = None
    hotelId: int
    totalAmount: Decimal
    status: str
    orderTime: datetime

class OrderDetailsResponse(BaseModel):
    id: int
    passengerId: int
    passengerName: str
    passengerPhone: str
    busNo: str
    email: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    seatNo: Optional[int] = None
    hotelId: int
    hotelName: str
    hotelLocation: str
    hotelPhone: str
    totalAmount: Decimal
    status: str
    orderTime: datetime

class PassengerOrderResponse(BaseModel):
    id: int
    passengerId: int
    hotelId: int
    hotelName: str
    hotelLocation: str
    totalAmount: Decimal
    status: str
    orderTime: datetime

class HotelOrderResponse(BaseModel):
    id: int
    passengerId: int
    passengerName: str
    passengerPhone: str
    busNo: str
    seatNo: Optional[int] = None
    hotelId: int
    totalAmount: Decimal
    status: str
    orderTime: datetime