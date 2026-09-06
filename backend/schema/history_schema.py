from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from fastapi import Query


class HistoryQueryParams:
    def __init__(
        self,
        start_time: datetime = Query(
            default=None,
            description="Filter orders from this time (e.g. 2026-08-27 10:00:00 or 2026-08-27)"
        ),
        end_time: datetime = Query(
            default=None,
            description="Filter orders up to this time (e.g. 2026-08-27 23:59:59 or 2026-08-27)"
        ),
        limit: int = Query(
            default=20,
            ge=1,
            le=100,
            description="Maximum number of orders to return"
        ),
        offset: int = Query(
            default=0,
            ge=0,
            description="Number of orders to skip for pagination"
        )
    ):
        self.start_time = start_time
        self.end_time = end_time
        self.limit = limit
        self.offset = offset


class OrderItemResponse(BaseModel):
    menuItemId: int
    menuItemName: str
    price: float
    quantity: int
    subtotal: float


class HotelOrderHistoryResponse(BaseModel):
    id: str
    hotelId: int
    passengerId: int
    orderId: int
    orderTimestamp: int
    items: List[OrderItemResponse]


class HotelOrderHistoryListResponse(BaseModel):
    hotelId: int
    totalOrders: int
    orders: List[HotelOrderHistoryResponse]