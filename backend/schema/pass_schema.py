from pydantic import BaseModel, field_validator
from typing import Optional

class PassengerCreate(BaseModel):
    name: str
    phone: str
    busNo: str 
    email: Optional[str] = None
    age: int 
    gender:str
    seatNo: Optional[int]= None

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, phone):
        if len(phone) != 10 or not phone.isdigit():
            raise ValueError(
                "Phone number must contain exactly 10 digits"
            )

        return phone

class PassengerUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    busNo: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    seatNo: Optional[int] = None

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, phone):
        if phone is not None:
            if len(phone) != 10 or not phone.isdigit():
                raise ValueError(
                    "Phone number must contain exactly 10 digits"
                )

        return phone

class PassengerResponse(BaseModel):
    id: int
    name: str
    phone: str
    busNo: str 
    email: Optional[str] = None
    age: int 
    gender:str
    seatNo: Optional[int]= None
