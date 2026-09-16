from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from backend.utils.jwt_utils import decode_access_token
from backend.repository.pass_repository import get_passenger_by_id
from backend.model.pass_model import Passenger

security = HTTPBearer()


def get_current_passenger(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Passenger:
   
    token = credentials.credentials

    try:
        payload = decode_access_token(token)
        passenger_id_str = payload.get("sub")
        if passenger_id_str is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload: missing passenger subject",
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
