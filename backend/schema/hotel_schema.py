from pydantic import BaseModel, field_validator


class HotelCreate(BaseModel):
    name: str
    location: str
    phone: str
    is_active: bool = True

    
    @field_validator("phone")
    @classmethod
    def validate_phone(cls, phone):
        if phone is not None:
            if len(phone) != 10 or not phone.isdigit():
                raise ValueError(
                    "Phone number must contain exactly 10 digits"
                )
    
        return phone

class HotelUpdate(BaseModel):
    name: str | None = None
    location: str | None = None
    phone: str | None = None
    is_active: bool | None = None

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, phone):
            if phone is not None:
                if len(phone) != 10 or not phone.isdigit():
                    raise ValueError(
                        "Phone number must contain exactly 10 digits"
                    )
        
            return phone


class HotelResponse(BaseModel):
    id: int
    name: str
    location: str
    phone: str
    is_active: bool