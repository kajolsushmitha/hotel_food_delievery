from fastapi import APIRouter, Depends, HTTPException, status
from backend.schema.auth_schema import (
    PassengerLoginRequest,
    TokenResponse,
    AuthenticatedOrderCreate
)
from backend.schema.pass_schema import PassengerResponse
from backend.schema.order_schema import OrderResponse, PassengerOrderResponse
from backend.services import auth_services
from backend.services.auth_services import PassengerNotFoundException
from backend.dependencies.auth_dependency import get_current_passenger
from backend.model.pass_model import Passenger

router = APIRouter(
    prefix="/auth/passenger",
    tags=["Passenger Authentication"]
)


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Passenger JWT Login",
    description="Logs in a passenger using their registered 10-digit phone number and returns a JWT access token."
)
def passenger_login(login_data: PassengerLoginRequest):
    try:
        return auth_services.login_passenger(login_data.phone)
    except PassengerNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )


@router.get(
    "/me",
    response_model=PassengerResponse,
    summary="Get Current Authenticated Passenger",
    description="Returns the profile details of the currently authenticated passenger extracted from the JWT token."
)
def get_current_passenger_profile(
    current_passenger: Passenger = Depends(get_current_passenger)
):
    return current_passenger


@router.get(
    "/orders",
    response_model=list[PassengerOrderResponse],
    summary="Get My Orders (Authenticated Passenger)",
    description="Fetches all orders placed by the currently authenticated passenger."
)
def get_my_orders(
    current_passenger: Passenger = Depends(get_current_passenger)
):
    try:
        return auth_services.get_authenticated_passenger_orders(
            current_passenger.id
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch orders: {str(e)}"
        )
