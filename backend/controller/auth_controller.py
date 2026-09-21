from fastapi import APIRouter, HTTPException, status
from backend.schema.auth_schema import (
    PassengerLoginRequest,
    TokenResponse,
    HotelLoginRequest,
    HotelTokenResponse
)
from backend.services import auth_services
from backend.services.auth_services import (
    PassengerNotFoundException,
    HotelNotFoundException
)

router = APIRouter(
    prefix="/auth/passenger",
    tags=["Passenger Authentication"]
)

hotel_auth_router = APIRouter(
    prefix="/auth/hotel",
    tags=["Hotel Authentication"]
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


@hotel_auth_router.post(
    "/login",
    response_model=HotelTokenResponse,
    summary="Hotel JWT Login",
    description="Logs in a hotel admin using their registered 10-digit hotel phone number and returns a JWT access token."
)
def hotel_login(login_data: HotelLoginRequest):
    try:
        return auth_services.login_hotel(login_data.phone)
    except HotelNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Hotel login failed: {str(e)}"
        )
