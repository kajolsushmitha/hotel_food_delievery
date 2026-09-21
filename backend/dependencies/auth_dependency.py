from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from backend.utils.jwt_utils import decode_access_token
from backend.repository.pass_repository import get_passenger_by_id
from backend.repository.hotel_repository import get_hotel_by_id
from backend.model.pass_model import Passenger

security = HTTPBearer()


def get_current_passenger(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Passenger:
   
    token = credentials.credentials

    try:
        payload = decode_access_token(token)
        passenger_id_str = payload.get("sub")
        role = payload.get("role")
        if passenger_id_str is None or (role is not None and role != "passenger"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload: missing or invalid passenger subject",
                headers={"WWW-Authenticate": "Bearer"},
            )
        passenger_id = int(passenger_id_str)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token has expired. Please log in again.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except (jwt.PyJWTError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials: invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    passenger = get_passenger_by_id(passenger_id)
    if passenger is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Passenger associated with this token no longer exists",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return passenger


def get_current_hotel(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    token = credentials.credentials

    try:
        payload = decode_access_token(token)
        hotel_id_str = payload.get("sub")
        role = payload.get("role")
        if hotel_id_str is None or role != "hotel":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload: missing or invalid hotel subject",
                headers={"WWW-Authenticate": "Bearer"},
            )
        hotel_id = int(hotel_id_str)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token has expired. Please log in again.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except (jwt.PyJWTError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials: invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    hotel = get_hotel_by_id(hotel_id)
    if hotel is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Hotel associated with this token no longer exists",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not hotel.get("is_active", True):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Hotel account is currently inactive",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return hotel
