from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field

class MenuItemCreate(BaseModel):
    name: str 
    description: Optional[str] = None
    price: Decimal = Field(..., gt=0)
    category: Optional[str] = Field(None, max_length=50)
    is_available: bool = True

class MenuItemUpdate(BaseModel):
    name: Optional[str] =None
    description: Optional[str] = None
    price: Optional[Decimal] = Field(None, gt=0)
    category: Optional[str] = Field(None, max_length=50)
    is_available: Optional[bool] = None

class MenuItemResponse(BaseModel):
    id: int
    hotelId: int
    name: str
    description: Optional[str]
    price: Decimal
    category: Optional[str]
    is_available: bool