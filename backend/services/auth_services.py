from backend.repository import pass_repository
from backend.services import order_services
from backend.schema.order_schema import OrderCreate
from backend.schema.auth_schema import AuthenticatedOrderCreate
from backend.utils.jwt_utils import create_access_token
from backend.model.pass_model import Passenger


class PassengerNotFoundException(Exception):
    def __init__(self, phone: str):
        self.message = f"Passenger with phone {phone} not found. Please register first."
        super().__init__(self.message)


def login_passenger(phone: str) -> dict:
   
    passenger = pass_repository.get_passenger_by_phone(phone)
    if passenger is None:
        raise PassengerNotFoundException(phone)

    token_data = {
        "sub": str(passenger.id),
        "phone": passenger.phone,
        "role": "passenger"
    }
    access_token = create_access_token(data=token_data)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "passenger": passenger
    }


def create_authenticated_passenger_order(
    current_passenger: Passenger,
    order_data: AuthenticatedOrderCreate
):
    
    full_order_data = OrderCreate(
        passengerId=current_passenger.id,
        hotelId=order_data.hotelId,
        totalAmount=order_data.totalAmount,
        items=order_data.items or []
    )
    return order_services.create_order(full_order_data)


def get_authenticated_passenger_orders(passenger_id: int):

    return order_services.get_orders_by_passenger(passenger_id)
